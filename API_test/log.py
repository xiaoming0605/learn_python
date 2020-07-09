import time
import os
PATH = os.path.split(os.path.realpath(__file__))[0]

class Log:
    def __init__(self,ID):
        self.id = ID
        self.logPath = os.path.join(PATH,r"log/"+time.strftime('%Y-%m-%d', time.localtime()))
        if not os.path.exists(self.logPath):
            try:
                os.makedirs(self.logPath)
            except:
                pass
        self.logname = os.path.join(self.logPath,time.strftime('%H%M', time.localtime())+"_"+str(self.id)+".log")
        self.alllog = os.path.join(self.logPath,time.strftime("%H", time.localtime())+"_all"+".log")
    def addlog(self,data):
        f = open(self.logname, 'a+',encoding='utf-8')
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '    ' + str(self.id) + data + '\n')
        f.close()
        f = open(self.alllog, 'a+',encoding='utf-8')
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '    ' + str(self.id) + data + '\n')
        f.close()
import logging
import time
import os

class mylog(object):
    def __init__(self,logger_name):

        #创建一个logger
        self.logger= logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)


        #设置日志存放路径，日志文件名
        #获取本地时间，转换为设置的格式
        rq = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        #设置所有日志和错误日志的存放路径
        all_log_path = os.path.join(os.path.dirname(os.getcwd()),'Logs/All_Logs/')
        error_log_path = os.path.join(os.path.dirname(os.getcwd()),'Logs/Error_Logs/')
        #设置日志文件名
        all_log_name = all_log_path + rq +'.log'
        error_log_name = error_log_path + rq +'.log'

        #创建handler
        #创建一个handler写入所有日志
        fh = logging.FileHandler(all_log_name)
        fh.setLevel(logging.INFO)
        #创建一个handler写入错误日志
        eh = logging.FileHandler(error_log_name)
        eh.setLevel(logging.ERROR)
        #创建一个handler输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        #定义日志输出格式
        #以时间-日志器名称-日志级别-日志内容的形式展示
        all_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #以时间-日志器名称-日志级别-文件名-函数行号-错误内容
        error_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s  - %(lineno)s - %(message)s')
        #将定义好的输出形式添加到handler
        fh.setFormatter(all_log_formatter)
        ch.setFormatter(all_log_formatter)
        eh.setFormatter(error_log_formatter)


        #给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(eh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger