# -*- coding: utf-8 -*-
################################################################################
#
# Author: ClimbSnail(HQ)
# original source is here.
#   https://github.com/ClimbSnail/HoloCubic_AIO
# 
#
################################################################################

import tkinter as tk
import tkutils as tku
from common import *
from ctypes import *  
from file_info import *
import sys


class FileManager(object):
    """
    菜单栏类
    """

    def __init__(self, father, engine, lock=None):
        """
        FileManager 初始化
        :param father:父类窗口
        :param engine:引擎对象，用于推送与其他控件的请求
        :param lock:线程锁
        :return:None
        """
        self.__engine = engine  # 负责各个组件之间数据调度的引擎
        self.__father = father  # 保存父窗口
        self.__file_pool = []    # 保存所有的目录信息
        fs = FileSystem_TT()
        recv_data = b'\x00\x01\x01\x00\x00\x00\x00'
        fs.decode(recv_data)
        print(fs.header_mark)
        # print(type(fs.action_type))
        # print(getSendInfo(fs.encode()))
        # print(sys.getsizeof(fs.file_name))

    def init_modelBar(self, menuBar):
        """
        初始化模型菜单子项
        :param menuBar: 主菜单
        :return: None
        """
        self.m_model_filepath = None
        # 创建菜单项
        self.modelBar = tk.Menu(menuBar, tearoff=0)
        # 将菜单项添加到菜单栏
        menuBar.add_cascade(label=self.__engine.word_map["Menu"]["Model"], menu=self.modelBar)
        # 在菜单项中加入子菜单
        self.modelBar.add_command(label=self.__engine.word_map["Menu"]["Create"], command=self.click_model_create)
        # 创建分割线
        self.modelBar.add_separator()

    def click_model_create(self):
        """
        点击模型"创建"菜单项触发的函数
        :return: None
        """
        print("click_model_create")
        # self.__engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_MODEL_FILEMANAGER,
        #                               mh.A_FILE_CREATE, self.m_model_filepath)
