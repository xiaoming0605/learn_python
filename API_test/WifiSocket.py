# {"errcode":62,"errmsg":"MD5 signature error"}
import readConfig
import WulinkInterface
import common

class WifiSocket(object):
    
    def __init__(self, ServerAddress, AppId, AppKey, wt, Token, DevId ,Post = readConfig.ReadConfig().get_SocketInfo('Post')):
        global DevType, LoginPwd
        global wulink_test
        global AccessToken
        global Query
        self.ID = DevId
        self.Post = Post
        Info = readConfig.ReadConfig()
        DevType = Info.get_SocketInfo('DevType')
        #DevId = Info.get_SocketInfo('DevId')
        LoginPwd = Info.get_SocketInfo('LoginPwd')
        Query = Info.get_SocketInfo('Query')
        #Post = Info.get_SocketInfo('Post')
        wulink_test = wt
        AccessToken = Token
        
    # 登录接口
    def LoginDev(self):
        return wulink_test.login(AccessToken, DevType, self.ID, LoginPwd)
    
    # 查询设备在线状态
    def GetOnlineStatus(self):
        return wulink_test.online_status(AccessToken, DevType, self.ID)
        
    # 查询设备接口状态
    def GetDevStatus(self):
        return wulink_test.get_method(AccessToken, DevType, self.ID, Query)
        
    def GetDevStatusV3(self):
        h_Post = common.HandlePost(self.Post)
        return wulink_test.get_methodV3(AccessToken, DevType, self.ID, h_Post)
    
    # V3设置设备接口状态
    def SetDevStatusV3(self):
        h_Post = common.HandlePost(self.Post)
        return wulink_test.set_methodV3(AccessToken, DevType, self.ID, h_Post)