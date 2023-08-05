#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/18 16:09
# @Blog    : https://blog.zbmain.com
import re

# 常用的类型
NUM = '0-9'
LETTERS = 'a-zA-Z'
NORMAL_CHAR = '!,.?！，。？'
SPECIAL_CHAR = '’"#$%&\'()*+-/;；<=>@★☆〇〖〗、【】＜＞《》“”‘’\\[\\\\]^_`{|}~'
CN_Unicode = '\u4E00-\u9FA5'#中文
CN_Unicdoe2 = '\u4E00-\u9FEF'#中文2


def clearNull(char: str):
    '''防止爬虫抓到特殊隐藏字符'''
    return re.sub(
        '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
        '', char)


def replaces(char: str, *regs, end=''):
    ccc = '[' + ''.join(regs) + ']'
    return re.sub(ccc, end, char)


if __name__ == "__main__":
    print(clearNull('123 abc 你好，世界！'))
    print(replaces('123 abc\你好\\世界！', NUM,LETTERS, NORMAL_CHAR, SPECIAL_CHAR, end='X'))
    print(replaces('123 @abc\你好，\n\世界！', '^',CN_Unicode,',，!！\n\0x0D\0x0A\u3000\u0020', end=''))
