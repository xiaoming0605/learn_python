# !/usr/bin/env python
# coding=utf-8

'''
物联云接口调用demo python版 Aes加密类
'''
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class prpcrypt():
    """
    AES加解密 128 ECB模式
    """
    def __init__(self,key):
        self.key = key
        
    def encrypt(self,text):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        unpad = lambda s : s[0:-ord(s[-1])]
        cipher = AES.new(self.key)
        return cipher.encrypt(pad(text)).encode('hex')
    
    def decrypt(self,text):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        unpad = lambda s : s[0:-ord(s[-1])]
        cipher = AES.new(self.key)
        return unpad(cipher.decrypt(text.decode('hex')))