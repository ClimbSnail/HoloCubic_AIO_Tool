# -*- coding: utf-8 -*-
################################################################################
#
# Author: ClimbSnail(HQ)
# original source is here.
#   https://github.com/ClimbSnail/HoloCubic_AIO
# 
#
################################################################################

from massagehead import *
import binascii
import re

VERSION = "Ver1.4.2"
ROOT_PATH = "OutFile"
CACHE_PATH = "Cache"


# 字节序定义
byteOrders = {'Native order':'@',   # 本机（默认）
            'Native standard':'=',  # 本机
            'Little-endian':'<',    # 小端
            'Big-endian':'>',       # 大端
            'Network order':'!'}    # network(大端)

# 关于struct格式串字节大小 https://blog.csdn.net/qq_30638831/article/details/80421019

def getSendInfo(info):
    """
    打印网络数据流, 
    :param info: ctypes.create_string_buffer()
    :return : str
    """
    info = binascii.hexlify(info)
    print(info)
    re_obj = re.compile('.{1,2}') #匹配任意字符1-2次
    t = ' '.join(re_obj.findall(str(info).upper()))
    return t