﻿# -*- coding: utf-8-*-
import os
import codecs
import struct
from cStringIO import StringIO


def getText():
    a_list = []
    base_str = u" !\"#$%　'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[＼]^_`abcdefghijklmnopqrstuvwxyz{|}~、。，．·：？！々ーー－／～…‘’“”（）［］「」『』【】＋－×＜＞％＆○□△※→←↑↓０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
    jis_str = u"ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶー"
    fl = os.listdir("cn-text")
    for fn in fl:
        fp = codecs.open("ko-text//%s" % fn, "rb", "utf-16")
        data = fp.read().replace("\r", "").replace("\n", "")
        for char in data:
            if char in base_str:
                pass
            elif char in jis_str:
                pass
            elif char in a_list:
                pass
            else:
                a_list.append(char)
        fp.close()
    dest = codecs.open("charlist.txt", "wb", "utf-16")
    dest.write(jis_str + "".join(a_list))
    dest.close()


def import_stringlistdatabase(string_list, o_data):
    br = StringIO()
    br.write(o_data)
    br.seek(0)
    nums = struct.unpack("I", br.read(4))[0]
    br.seek(0x10 * nums, 1)
    br.truncate()
    for i in xrange(nums):
        br.seek(0, 2)
        ofs = br.tell()
        string = string_list[i].replace("\r", "")
        br.write(string.encode("utf-8"))
        br.write("\x00\x00")
        br.seek(0x4 + 0x10 * i + 0x4)
        br.write(struct.pack("I", len(string)))
        br.write(struct.pack("I", ofs-4))
    return br.getvalue()


def import_keyitemdatabase(string_list, o_data):
    br = StringIO()
    br.write(o_data)
    br.seek(0)
    nums = struct.unpack("I", br.read(4))[0]
    br.seek(0x10 * nums, 1)
    br.truncate()
    for i in xrange(nums):
        br.seek(0, 2)
        ofs = br.tell()
        string = string_list[i].replace("\r", "")
        br.write(string.encode("utf-8"))
        br.write("\x00\x00")
        br.seek(0x4 + 0x10 * i + 0x4)
        br.write(struct.pack("I", len(string)))
        br.write(struct.pack("I", ofs - 4))
    return br.getvalue()


def makestr(lines):
    string_list = []
    head_list = []
    num = len(lines)
    for index, line in enumerate(lines):
        if u'####' in line:
            head_list.append(line[5:-7])
            i = 1
            string = ''
            while True:
                if index + i >= num:
                    break
                if '####' in lines[index + i]:
                    break
                string += lines[index + i]
                i += 1
            string_list.append(string[:-2])
    return string_list


def build_text(name):
    print(name)
    fp = open("data//%s" % name, "rb")
    data = fp.read()
    text = codecs.open("ko-text//%s.txt" % name, "rb", "utf-16").readlines()
    text = makestr(text)
    if ("collectionitemdatabase" in name):
        dst = import_keyitemdatabase(text, data)
    elif ("keyitemdatabase" in name):
        dst = import_keyitemdatabase(text, data)
    else:
        dst = import_stringlistdatabase(text, data)
    if not os.path.exists("import"):
        os.makedirs("import")
    dest = open("import//%s" % name, "wb")
    dest.write(dst)
    dest.close()
    fp.close()
    pass


def main():
    #getText()
    build_text("StringListDataBase_en.dat")

if __name__ == "__main__":
    main()
