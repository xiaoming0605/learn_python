# ###########################################

# ###########################################

import os
import codecs
import configparser

# 获取当前文件readConfig.py的所在目录
PATH = os.path.split(os.path.realpath(__file__))[0]


# 获取配置文件config.ini的路径
config_Path = os.path.join(PATH, "config.ini")

# 获取配置文件信息
class ReadConfig(object):
    
    def __init__(self):
        fd = open(config_Path)
        data = fd.read()
        fd.close()
        
        self.cf = configparser.ConfigParser()
        self.cf.read(config_Path)
    
    # 获取基本信息
    def get_EssentialInfo(self, name):
        value = self.cf.get("EssentialInfo", name)
        return value

    # 获取插座信息
    def get_SocketInfo(self, name):
        value = self.cf.get("SocketInfo", name)
        return value
        