import WulinkInterface

# 获取token
def GetToken(wulink_test, appkey):
    token = wulink_test.get_tokenV3(appkey)
    return HandleToken(token)

# 更新token
def UpdataToken(wulink_test, appkey):
    token = wulink_test.update_tokenV3(appkey)
    return HandleToken(token)

# 处理token
def HandleToken(token):
    token = eval(token)
    if token['errcode'] == 0:
        return token['data']['access_token']
    return token

# 将post字符串形式转化成字典    
def HandlePost(post):
    return eval(post)