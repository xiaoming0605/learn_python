import readConfig
import WulinkInterface
from WifiSocket import *
import common
import log
import re
import time
import threading,random
from Helper import *


class Allrun(object):

    def __init__(self, DevId):
        # 基本变量
        global ServerAddress, AppId, AppKey
        global wulink_test
        global AccessToken
        self.DevId = DevId
        ServerAddress = readConfig.ReadConfig().get_EssentialInfo('ServerAddress')
        AppId = readConfig.ReadConfig().get_EssentialInfo('AppId')
        AppKey = readConfig.ReadConfig().get_EssentialInfo('AppKey')
        self.post = readConfig.ReadConfig().get_SocketInfo('Post').split(';')
        self.LOG = log.Log(self.DevId)
        self.LOG.addlog(" 开始测试")
        wulink_test = WulinkInterface.WulinkInterface(ServerAddress, AppId)
        # 获得token
        self.LOG.addlog(' ServerAddress:%s    AppId:%s' %(ServerAddress,AppId))
        #AccessToken = common.UpdataToken(wulink_test, AppKey)
        AccessToken = common.GetToken(wulink_test, AppKey)
        if isinstance(AccessToken, dict):
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), "Token is invalid，Update Token!")
            self.LOG.addlog(" Token is invalid，UpdateToken!")
            AccessToken = common.UpdataToken(wulink_test, AppKey)
            self.LOG.addlog(" UpdataToken!")
        self.LOG.addlog(" AccessToken:%s" % AccessToken)
    # 执行
    def run(self,p):
        global AccessToken
        t = WifiSocket(ServerAddress, AppId, AppKey, wulink_test, AccessToken, self.DevId ,p)
        rep = t.GetDevStatusV3()
        if re.search(r'Error',rep)!= None or re.search(r'LAST_DATA',rep)!= None or re.search(r'wait',rep)!= None or re.search(r'Device',rep)!= None:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),str(self.DevId),rep)
            self.LOG.addlog(" ERROR %s"%rep)
        elif re.search(r'"errcode":1001',rep) != None:
            self.LOG.addlog(" ERROR %s"%rep)
            AccessToken = common.UpdataToken(wulink_test, AppKey)
            self.LOG.addlog(" Token is invalid，Update Token!")
            self.LOG.addlog(" new Token:%s"%AccessToken)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),"Token is invalid，Update Token!")
        elif re.search(r'"errcode":62',rep) != None:
            self.LOG.addlog(" ERROR %s"%rep)
            AccessToken = common.GetToken(wulink_test, AppKey)
            self.LOG.addlog(" Token has been updated，Get new Token!")
            self.LOG.addlog(" new Token:%s"%AccessToken)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),"Token has been updated，Get new Token!")
        elif re.search(r'"errcode":0',rep) == None:
            self.LOG.addlog(" ERROR %s"%rep)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),"Other error!",rep)
        else:
            self.LOG.addlog(rep)
P = readConfig.ReadConfig().get_SocketInfo('Post').split(';')

def test(sn):
    obj = Allrun(sn)
    for n in range(1,10000,len(obj.post)):
        for i in range(len(obj.post)):
            obj.LOG.addlog(' 第%s次测试    Post:%s'% ((n+i),obj.post[i]))
            obj.run(obj.post[i])
            time.sleep(120/len(obj.post))
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), "+++++++++ OVER +++++++++")
    
def threads_join(threads):
    '''
    令主线程阻塞，等待子线程执行完才继续，使用这个方法比使用join的好处是，可以ctrl+c kill掉进程
    '''
    for t in threads:
        while True:
            if t.isAlive():
                time.sleep(10)
            else:
                break

if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), "开始测试")
    threadpool = []
    th = threading.Thread(target=test, args=(267100000007,))
    threadpool.append(th)
    for i in range(267100000048,267100000076):
        th = threading.Thread(target=test, args=(i,))
        threadpool.append(th)
    for th in threadpool:
        th.setDaemon(True)
        th.start()
        #time.sleep(random.randint(1,3))
    #join方式不能实现ctrl+c kill掉进程
    # for th in threadpool:
        # threading.Thread.join(th)
    threads_join(threadpool)
    print('Ctrl+C')