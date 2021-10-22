# -*- coding: utf-8 -*-
################################################################################
#
# Author: ClimbSnail(HQ)
# original source is here.
#   https://github.com/ClimbSnail/HoloCubic_AIO
# 
#
################################################################################

from common import *
from ctypes import *
import struct 


class ActionType:
    class ConstError(TypeError): pass

    # 目录操作
    AT_DIR_CREATE = 0  # 创建
    AT_DIR_REMOVE = 1   # 删除
    AT_DIR_RENAME = 2   # 重命名
    AT_DIR_LIST = 3   # 列举目录文件

    # 文件操作
    AT_FILE_CREATE = 100  # 创建
    AT_FILE_WRITE = 101  # 文件信息流写
    AT_FILE_READ = 102  # 文件信息读
    AT_FILE_REMOVE = 103   # 删除
    AT_FILE_RENAME = 104   # 重命名
    AT_FILE_GET_INFO = 105   # 查询文件大小

    def __setattr__(self, name, value):
        raise self.ConstError(f"Can't rebind const {name}")

AT = ActionType()

class FileSystem_T(MsgHead_T):
    
    def __init__(self):
        MsgHead_T.__init__(self)
        self.action_type = AT.AT_DIR_CREATE
        self.__fmt = "1B"
        self.__size = struct.Struct(self.__fmt).size

    def decode(self, network_data, byteOrder = '@'):
        super().decode(network_data, byteOrder)
        get_data = struct.unpack(byteOrder+self.__fmt, network_data[super().__size : super().__size+self.__size])
        self.action_type = get_data[0]

    def encode(self, byteOrder = '!'):
        # buffer = ctypes.create_string_buffer(bufferLength) # 创建发送缓冲区
        super_data = super().encode(byteOrder)
        return super_data + struct.pack(byteOrder+self.__fmt, self.action_type)

class FileSystem_TT(MsgHead_TT):
    
    def __init__(self):
        MsgHead_TT.__init__(self)
        self.action_type = AT.AT_DIR_CREATE
        print(self.fmt)
        self.fmt = self.fmt+"1B"
        print(self.fmt)


class FileSystem(Structure):
    # _fields_ = [
    #         # ("msg_head", MsgHead),
    #         ("action_type",c_byte)
    #         ]
    _fields_ = MsgHead._fields_
    _fields_.extend([("action_type",c_byte)]) 


class FileCreate(Structure):
    _fields_ = FileSystem._fields_
    extend_param = [
            ("file_system", FileSystem),
            ("file_name",c_byte*99),
            ("file_size",c_uint)
            ]
    _fields_.extend(extend_param)


class FileWrite(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_data",c_byte*65536)
            ]


class FileRead(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_data",c_byte*65536)
            ]


class FileRemove(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_name",c_byte*99)
            ]


class FileRename(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_cur_name", c_byte*99),
            ("file_new_name", c_byte*99)
            ]


class FileGetInfo(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_name",c_byte*99),
            ("file_info",c_byte*99)
            ]


class DirCreate(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_name",c_byte*99)
            ]


class DirRemove(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_name",c_byte*99)
            ]


class DirRename(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("dir_cur_name", c_byte*99),
            ("dir_new_name", c_byte*99)
            ]


class DirList(Structure):
    _fields_ = [
            ("file_system", FileSystem),
            ("file_name", c_byte*99),
            ("dir_info", c_byte*3000)
            ]