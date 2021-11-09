#-*- coding:utf-8 -*-
import codecs
import os
import struct
from cStringIO import StringIO


def export_stringlistdatabase(data):
    br = StringIO(data)
    br.seek(0)
    dst_lst = []
    id_list = []
    magic_lst =[]
    nums = struct.unpack("I", br.read(4))[0]
    print(hex(nums))
    for i in xrange(nums):
        br.seek(0x4 + 0x10 * i)#요마와리는 0x4+0xC*i 신요마와리는 0x4+0x10*i) 매직넘버가 글씨체 같은것을 의미하는 듯 하다
        _id = struct.unpack("I", br.read(4))[0]
        _char_num = struct.unpack("I", br.read(4))[0]
        _offset = struct.unpack("I", br.read(4))[0]
        _offset += 4
        _magic = struct.unpack("I", br.read(4))[0]
        br.seek(_offset)
        print(hex(_offset))
        string = br.read(_char_num * 3 + 2).split("\x00\x00")[0]
        string = string.split("\x00")[0]
        print(string)
        string = string.decode("utf-8")
        string = string.replace("\r", "")
        #string = string.replace("\n", "\r\n")
        dst_lst.append(string)
        id_list.append(_id)
        magic_lst.append(_magic)
    return dst_lst


def export_keyitemdatabase(data):
    br = StringIO(data)
    br.seek(0)
    dst_lst = []
    nums = struct.unpack("I", br.read(4))[0]
    for i in xrange(nums):
        br.seek(0x4 + 0x10 * i)
        _id = struct.unpack("I", br.read(4))[0]
        _char_num = struct.unpack("I", br.read(4))[0]
        _offset = struct.unpack("I", br.read(4))[0]
        _id1 = struct.unpack("I", br.read(4))[0]
        _offset += 4
        br.seek(_offset)
        print(hex(_offset))
        string = br.read(_char_num * 3 + 2).split("\x00\x00")[0]
        string = string.decode("utf-8")
        #print(string)
        string = string.replace("\r", "")
        #string = string.replace("\n", "\r\n")
        dst_lst.append(string)
    return dst_lst


def export_text(name):
    print(name)
    fp = open("data//%s" % name, "rb")
    data = fp.read()
    if ("collectionitemdatabase" in name):
        lst = export_keyitemdatabase(data)
    elif ("keyitemdatabase" in name):
        lst = export_keyitemdatabase(data)
    else:
        lst = export_stringlistdatabase(data)
    dst = codecs.open("jp-text//%s.txt" % name, "wb", "utf-16")
    for i in xrange(len(lst)):
        string = lst[i]
        dst.write(u"#### %d ####\n%s\n\n" % (i + 1, string))
    dst.close()
    fp.close()

#export_text("StringListDataBase_en.dat")
export_text("StringListDataBase_en.dat")
