# !/usr/bin/env python
# coding=utf-8

'''
物联云接口调用demo python版
'''

import urllib,random,json,hashlib


class Helper(object):
      
    def createRandom(self,length = 16):
        pattern = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ'
        str = ''
        i = 0
        while i < length:
            str = str + pattern[random.randint(0,61)]
            i += 1
        return str
    
    def caculate_sign(self, appid, token, nonce, time, post = False):
        sign = appid + str(token) + nonce + time
        if post:
            sign += post
        ret = hashlib.md5(sign.encode("utf8")).hexdigest()
        return ret