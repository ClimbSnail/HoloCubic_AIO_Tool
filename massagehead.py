# -*- coding: utf-8 -*-
################################################################################
#
# Author: ClimbSnail(HQ)
# original source is here.
#   https://github.com/ClimbSnail/HoloCubic_AIO
# 
#
################################################################################

from ctypes import *
from common import *
import struct 

# 模块名 M_
M_ALL = "M_ALL"
M_ENGINE = "M_ENGINE"
M_DOWNLOAD_DEBUG = "M_DOWNLOAD_DEBUG"
M_SETTING = "M_SETTING"
M_FILE_MANAGER = "M_FILE_MANAGER"
M_PICTURE = "M_PICTURE"
M_VIDEO_TOOL = "M_VIDEO_TOOL"
M_SRCEEN_SHARE = "M_SRCEEN_SHARE"
M_HELP = "M_HELP"

# 动作类型 A_
A_UPDATALANG = "A_UPDATALANG"
A_CREATE_MODEL = "A_CREATE_MODEL"


class ModuleType:
    class ConstError(TypeError): pass

    # 模块名 Holocubic
    CUBIC_FILE_MANAGER = 0

    # 上位机控制器
    C_FILE_MANAGER = 1

    def __setattr__(self, name, value):
        raise self.ConstError(f"Can't rebind const {name}")

MT = ModuleType()   # 模块类型

class MsgHead(Structure):
    _fields_ = [
            ("header_mark",c_byte*2),
            ("from_who",c_byte),
            ("to_who",c_byte),
            ("msg_len",c_uint),
            ]


class MsgHead_T():

    def __init__(self):
        self.header_mark = 0
        self.from_who = MT.C_FILE_MANAGER
        self.to_who = MT.CUBIC_FILE_MANAGER
        self.msg_len = 0
        self.__fmt = "1H1B1B1H"
        self.__size = struct.Struct(self.__fmt).size

    def decode(self, network_data, byteOrder = '@'):
        get_data = struct.unpack(byteOrder+self.__fmt, network_data[ : self.__size])
        self.header_mark = get_data[0]
        self.from_who = get_data[1]
        self.to_who = get_data[2]
        self.msg_len = get_data[3]

    def encode(self, byteOrder = '!'):
        # buffer = ctypes.create_string_buffer(bufferLength) # 创建发送缓冲区
        return struct.pack(byteOrder+self.__fmt, self.header_mark, self.from_who,
            self.to_who, self.msg_len)


class MsgHead_TT():

    def __init__(self):
        self.header_mark = 0
        self.from_who = MT.C_FILE_MANAGER
        self.to_who = MT.CUBIC_FILE_MANAGER
        self.msg_len = 0
        self.fmt = "1H1B1B1H"

    def decode(self, network_data, byteOrder = '@'):
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr.startswith("fmt")]
        print(members)
        size = struct.Struct(self.fmt).size
        get_data = struct.unpack(byteOrder+self.fmt, network_data[ : size])
        for (attr, value) in zip(members, get_data):
        # for attr in members:
            getattr(self, attr, value)

    def encode(self, byteOrder = '!'):
        # buffer = ctypes.create_string_buffer(bufferLength) # 创建发送缓冲区
        return struct.pack(byteOrder+self.fmt, self.header_mark, self.from_who,
            self.to_who, self.msg_len)


# 结构体转字典
def dump_dict(obj):
    info = {}
    # 通过_fields_获取每一个字段
    # 检查每个字段的类型，根据不同类型分别处理
    # 支持递归迭代
    for k, v in obj._fields_:
        av = getattr(obj, k)
        if type(v) == type(Structure):
            print(av)
            # av = av.dump_dict()
        elif type(v) == type(Array):
            av = cast(av, c_char_p).value.decode()
        else:
            pass
        info[k] = av
    return info