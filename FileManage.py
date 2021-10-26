# -*- coding: utf-8 -*-
__author__ = 'Yang'

from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk

class Application_UI(object):
    
    # path = r"E:\\python开发工具\\project\\tkinter"
    path = os.path.abspath(".")
    file_types = [".png", ".jpg", ".jpeg", ".ico", ".gif"]
    scroll_visiblity = True
    
    font = 11
    font_type = "Courier New"
    
    def __init__(self):
        # 设置UI界面
        window = Tk()
        self.root = window
        win_width = 800
        win_height = 600
        
        screen_width, screen_height = window.maxsize() 
        x = int((screen_width - win_width) / 2)
        y = int((screen_height - win_height) / 2)
        window.title("文件管理工具")
        window.geometry("%sx%s+%s+%s" % (win_width, win_height, x, y))
        
        menu = Menu(window)
        window.config(menu = menu)
        
        selct_path = Menu(menu, tearoff = 0)
        selct_path.add_command(label = "打开", accelerator="Ctrl + O", command = self.open_dir)
        selct_path.add_command(label = "保存", accelerator="Ctrl + S", command = self.save_file)
        
        menu.add_cascade(label = "文件", menu = selct_path)
        
        about = Menu(menu, tearoff = 0)
        about.add_command(label = "版本", accelerator = "v1.0.0")
        about.add_command(label = "作者", accelerator = "样子")
        menu.add_cascade(label = "关于", menu = about)
        
        # 顶部frame
        top_frame = Frame(window, bg = "#fff")
        top_frame.pack(side = TOP, fill = X)
        label = Label(top_frame, text = "当前选中路径：", bg = "#fff")
        label.pack(side = LEFT)
        
        self.path_var = StringVar()
        self.path_var.set("无")
        label_path = Label(top_frame, textvariable = self.path_var, bg = "#fff", fg = "red", height = 2)
        label_path.pack(anchor = W)
        
        
        paned_window = PanedWindow(window, showhandle = False, orient=HORIZONTAL)
        paned_window.pack(expand = 1, fill = BOTH)
        
        # 左侧frame
        self.left_frame = Frame(paned_window)
        paned_window.add(self.left_frame)
        
        self.tree = ttk.Treeview(self.left_frame, show = "tree", selectmode = "browse")
        tree_y_scroll_bar = Scrollbar(self.left_frame, command = self.tree.yview, relief = SUNKEN, width = 2)
        tree_y_scroll_bar.pack(side = RIGHT, fill = Y)
        self.tree.config(yscrollcommand = tree_y_scroll_bar.set)
        self.tree.pack(expand = 1, fill = BOTH)
        
                
        # 右侧frame
        right_frame = Frame(paned_window)
        paned_window.add(right_frame)
        
        # 右上角frame
        right_top_frame = Frame(right_frame)
        right_top_frame.pack(expand = 1, fill = BOTH)
        
        self.number_line = Text(right_top_frame, width = 0, takefocus = 0, border = 0, font = (self.font_type, self.font), cursor = "") 
        self.number_line.pack(side = LEFT, fill = Y)
        
        
        # 右上角Text
        text = Text(right_top_frame, font = (self.font_type, self.font), state = DISABLED, cursor = "", wrap = NONE)
        self.text_obj = text
        text_x_scroll = Scrollbar(right_frame, command = text.xview, orient = HORIZONTAL)
        text_y_scroll = Scrollbar(right_top_frame, command = text.yview)
        self.text_scroll_obj = text_y_scroll
        text.config(xscrollcommand = text_x_scroll.set, yscrollcommand = text_y_scroll.set)
        text_y_scroll.pack(side = RIGHT, fill = Y)
        text_x_scroll.pack(side = BOTTOM, fill = X)
        text.pack(expand = 1, fill = BOTH)
        
    
        # 右下角frame
        right_bottom_frame = Frame(right_frame)
        right_bottom_frame.pack(side = BOTTOM, fill = X)
        
        self.folder_img = PhotoImage(file = r"./image/folder.png")
        self.file_img = PhotoImage(file = r"./image/text_file.png")
        
        php_img = PhotoImage(file = r"./image/php.png")
        python_img = PhotoImage(file = r"./image/python.png")
        image_img = PhotoImage(file = r"./image/img.png")
        
        
        # 设置文件图标
        self.icon = {".php": php_img, ".py": python_img, ".pyc": python_img, ".png": image_img, ".jpg": image_img, ".jpeg": image_img, ".gif": image_img, ".ico": image_img}
        
        # 加载目录文件
        self.load_tree("", self.path)
        self.tree.bind("<<TreeviewOpen>>", lambda event: self.select_tree())
        text.bind("<MouseWheel>", lambda event : self.update_line())
        
        self.number_line.bind("<FocusIn>", self.focus_in_event)
        self.number_line.bind('<Button-1>', self.button_ignore)
        self.number_line.bind('<Button-2>', self.button_ignore)
        self.number_line.bind('<Button-3>', self.button_ignore)
        self.number_line.bind('<B1-Motion>', self.button_ignore)
        self.number_line.bind('<B2-Motion>', self.button_ignore)
        self.number_line.bind('<B3-Motion>', self.button_ignore)
        
        self.text_scroll_obj.bind('<B1-Motion>', lambda event: self.update_line())
        self.text_obj.bind('<KeyRelease>', lambda event: self.update_line())
        
        text.bind("<Control-Key-s>", lambda event: self.save_file())
        text.bind("<Control-Key-S>", lambda event: self.save_file())
        text.bind("<Control-Key-Z>", lambda event: self.toUndo())
        text.bind("<Control-Key-Y>", lambda event: self.toRedo())
        
        window.mainloop()

class Application(Application_UI):
    def __init__(self):
        Application_UI.__init__(self)
    
    
    ''' 保存文件'''
    def save_file(self):
        # 判断是否是文件
        path = self.path_var.get()
        print(path)
        if self.is_file(path) is True:
            # 判断是否为图片
            if self.is_type_in(path) is False:
                content = self.text_obj.get(1.0, END)[:-1]
                with open(path, "w", encoding = "utf-8") as f:
                    f.write(content)
                messagebox.showinfo("提示", "保存成功")
            else:
                messagebox.showwarning("提示", "不能保存图片")
        else:
            messagebox.showwarning("提示", "不能保存目录")
            
    ''' 设置默认搜索路径'''
    def open_dir(self):
        path = filedialog.askdirectory(title = u"设置目录", initialdir = self.path)
        print("设置路径："+path)
        self.path = path
        # 删除所有目录
        self.delete_tree()
        self.load_tree("", self.path)
    
    ''' 判断是否为文件'''
    def is_file(self, path):
        if os.path.isfile(path):
           return True
        return False
    
    ''' 判断是否是图片类型'''
    def is_type_in(self, path):
        ext = self.file_extension(path)
        if ext in self.file_types:
            return True
        return False
    
    ''' 删除树'''
    def delete_tree(self):
        self.tree.delete(self.tree.get_children())
    
    def focus_in_event(self, event=None):
        self.text_obj.focus_set()
    
    def button_ignore(self, ev=None):
        return "break"
    
    ''' 加载目录'''
    def load_tree(self, root, path):
        is_open = False
        if root == "":
            is_open = True
        
        root = self.tree.insert(root, END, text = " " + self.dir_name(path), values = (path,), open = is_open, image = self.folder_img)    
        
        try:
            for file in os.listdir(path):
                file_path = path + "\\" + file
                if os.path.isdir(file_path):
                    self.load_tree(root, file_path)
                else:
                    ext = self.file_extension(file)
                    img = self.icon.get(ext)
                    if img is None:
                        img = self.file_img
                    self.tree.insert(root, END, text = " " + file, values = (file_path,), image = img)
        except Exception as e:
            print(e)
            
    ''' 获取文件后缀'''
    def file_extension(self, file):
        file_info = os.path.splitext(file)
        return file_info[-1]
    
    ''' 获取目录名称'''
    def dir_name(self, path):
        path_list = os.path.split(path)
        return path_list[-1]
    
    ''' 更新行数'''
    def update_line(self):
        if not self.scroll_visiblity:
            return 
        self.number_line.delete(1.0, END)
        text_h, text_l = map(int, str.split(self.text_obj.index(END), "."))
        q = range(1, text_h)
        r = map(lambda x: '%i' % x, q)
        s = '\n'.join(r)
        self.number_line.insert(END, s)
        
        if text_h <= 100:
            width = 2
        elif text_h <= 1000:
            width = 3
        elif text_h <= 10000:
            width = 4
        else:
            width = 5
        self.number_line.configure(width = width)
        self.number_line.yview_moveto(self.text_obj.yview()[0])
        
    ''' 选中item回调'''
    def select_tree(self):
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            select_path = "\\".join(item_text)
            self.path_var.set(select_path)
            
            self.text_obj.config(state = NORMAL, cursor = "xterm")
            # 清空text内容
            self.text_obj.delete(1.0, END)
            self.update_line()
            if self.is_file(select_path) is True:
                if self.is_type_in(select_path) is True:
                    self.text_obj.config(state = DISABLED, cursor = "")
                    self.look_image(select_path)
                else:
                    try:
                        self.open_file(select_path, "r", "utf-8")
                        self.update_line()
                    except Exception as e:
                        print(e)
            else:
                self.text_obj.config(state = DISABLED, cursor = "")
                
    ''' 查看图片'''
    def look_image(self, select_path):
        try:
            image = Image.open(select_path)
            self.look_photo = ImageTk.PhotoImage(image)
            self.text_obj.image_create(END, image = self.look_photo)
        except Exception as e:
            print(e)
    
    ''' 打开文件写入内容'''
    def open_file(self, select_path, mode, encoding = None):
        with open(select_path, mode = mode, encoding = encoding) as f:
            self.text_obj.insert(1.0, f.read())

if __name__ == "__main__":
    Application()

