# !/usr/bin/env python
# coding=utf-8

'''
物联云接口调用demo python版
'''

import urllib.request,urllib.parse,time,hashlib,socket,urllib.error
from Helper import *
from prpcrypt import *
import re

# yyl测试加入：查询和更新token时，不认证浏览器，避免失败
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def Merge(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res 

class WulinkInterface(object):
    
    def __init__(self, testip, appid):
      self.testip = testip
      self.appid = appid
    
    def get_tokenV3(self,appkey):
        #获取token
        if re.search(':',self.testip)!= None:
            url = "http://%s/v3/access/token" % self.testip
        else:
            url = "https://%s/v3/access/token" % self.testip
        params = {'appid': self.appid, 'appkey': appkey}
        params = urllib.parse.urlencode(params)
        try:
            ret_data = urllib.request.urlopen("%s?%s"%(url, params),timeout=80).read().decode('utf-8')
            return ret_data
        # except urllib.error.URLError as e:
            # if hasattr(e,'code'):
                # print(" HTTPError:",str(e))
            # elif hasattr(e,'reason'):
                # print(" URLError:" ,str(e))
        except Exception as e:
            print(e)
    
    def update_tokenV3(self,appkey):
        #更新token
        if re.search(':',self.testip)!= None:
            url = "http://%s/v3/access/token" % self.testip
        else:
            url = "https://%s/v3/access/token" % self.testip
        params = {'appid': self.appid, 'appkey': appkey}
        jdata = json.dumps(params)
        headers = {'Content-Type': 'application/json'}
        request = urllib.request.Request(url, headers=headers, data = jdata.encode(encoding='utf-8'))
        try:
            ret_data = urllib.request.urlopen(request,timeout=80).read().decode('utf-8')
            return ret_data
        # except urllib.error.URLError as e:
            # if hasattr(e,'code'):
                # print(" HTTPError:",str(e))
            # elif hasattr(e,'reason'):
                # print(" URLError:" ,str(e))
        except Exception as e:
            print(e)
    
    def login(self,token, devtype, devid, login_pws):
        #登录接口
        hh = Helper()
        nonce = hh.createRandom() #随机字符串，用于签名
        cur_time = int(time.time()) #时间戳，自1970-01-01的0时至今的秒数，用于签名以及请求时间窗口验证
        url = "http://%s/v1/%s/%s/passwd.json" % (self.testip, devtype, devid)
        dataKey = hashlib.md5(token.encode("utf8")).hexdigest()[0:16]  #进行aes加密的秘钥
        aec_instance = prpcrypt(dataKey);
        post_pwd = urllib.parse.urlencode({'passwd':aec_instance.encrypt(login_pws)})
        sign = hh.caculate_sign(self.appid, token, nonce, str(cur_time), post_pwd)
        get_paramp = {'timestamp': cur_time, 'nonce': nonce, 'appid': self.appid, 'sign': sign}
        
        params = urllib.parse.urlencode(get_paramp)
        ret = urllib.request.urlopen("%s?%s" % (url, params), post_pwd)
        ret_data = ret.read()
        return ret_data
    
    def online_status(self, token, devtype, devid):
        #查询设备在线接口
        hh = Helper()
        nonce = hh.createRandom() #随机字符串，用于签名
        cur_time = int(time.time()) #时间戳，自1970-01-01的0时至今的秒数，用于签名以及请求时间窗口验证
        url = "http://%s/v1/%s/%s/online.json" % (self.testip, devtype, devid)
        dataKey = hashlib.md5(token.encode("utf8")).hexdigest()[0:16]  #进行aes加密的秘钥
        aec_instance = prpcrypt(dataKey);
        sign = hh.caculate_sign(self.appid, token, nonce, str(cur_time))
        get_paramp = {'timestamp': cur_time, 'nonce': nonce, 'appid': self.appid, 'sign': sign}
        params = urllib.parse.urlencode(get_paramp)
        try:
            ret_data = urllib.request.urlopen("%s?%s" % (url, params),timeout=80).read().decode('utf-8')
        # except urllib.error.URLError as e:
            # if hasattr(e,'code'):
                # ret_data = " HTTPError:" + str(e)
            # elif hasattr(e,'reason'):
                # ret_data = " URLError:" + str(e)
        except Exception as e:
            ret_data = str(e)
        return ret_data
    
    def get_methodV3(self, token, devtype, devid, post):
        #查询设备状态接口
        hh = Helper()
        nonce = hh.createRandom() #随机字符串，用于签名
        cur_time = int(time.time()) #时间戳，自1970-01-01的0时至今的秒数，用于签名以及请求时间窗口验证
        if self.testip == 'api.galaxywind.com':
            url = "https://%s/v3/apartment/%s" % (self.testip, devid)
        elif self.testip == 'api.ifanscloud.com':
            url = "https://%s/v3/device/%s" % (self.testip, devid)
        else:
            url = "http://%s/v3/apartment/%s" % (self.testip, devid)
        # dataKey = hashlib.md5(token.encode("utf8")).hexdigest()[0:16]  #进行aes加密的秘钥
        # aec_instance = prpcrypt(dataKey);
        sign = hh.caculate_sign(self.appid, token, nonce, str(cur_time))
        get_paramp = {"appid":self.appid,'nonce':nonce,'timestamp':cur_time,'sign':sign,'devtype':devtype,"cmdtype":"get"}
        new_get_paramp = Merge(get_paramp,post)
        params = urllib.parse.urlencode(new_get_paramp)
        try:
            ret_data = urllib.request.urlopen("%s?%s" % (url, params),timeout=80).read().decode('utf-8')
        # except urllib.error.URLError as e:
            # if hasattr(e,'code'):
                # ret_data = " HTTPError " + str(e)
            # elif hasattr(e,'reason'):
                # ret_data = " URLError " + str(e)
        except Exception as e:
            ret_data = str(e)
        return ret_data

    def set_methodV3(self, token, devtype, devid, post):
        #V3设置设备状态接口
        hh = Helper()
        nonce = hh.createRandom()
        cur_time = int(time.time())
        if self.testip == 'api.galaxywind.com':
            url =  "https://%s/v3/apartment/%s" % (self.testip, devid)
        elif self.testip == 'api.ifanscloud.com':
            url =  "https://%s/v3/device/%s" % (self.testip, devid)
        sign = hh.caculate_sign(self.appid, token, nonce, str(cur_time))
        post0 = {"appid":self.appid,'nonce':nonce,'timestamp':cur_time,'sign':sign,'devtype':devtype,"cmdtype":"set"}
        newpost = Merge(post0,post)
        #jdata = urllib.parse.urlencode(newpost) #post数据url格式
        #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        jdata = json.dumps(newpost) #post数据json格式
        headers = {'Content-Type': 'application/json'}
        request = urllib.request.Request(url, headers=headers, data = jdata.encode(encoding='utf-8'),timeout=80)
        try:
            ret_data = urllib.request.urlopen(request).read().decode('utf-8')
        # except urllib.error.URLError as e:
            # if hasattr(e,'code'):
                # ret_data = " HTTPError " + str(e)
            # elif hasattr(e,'reason'):
                # ret_data = " URLError " + str(e)
        except Exception as e:
            ret_data = str(e)
        return ret_data