from itchat.content import *
import requests
import json
import itchat

groups = []

itchat.auto_login(hotReload=True,enableCmdQR=2)
# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
    appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer

# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
    df = itchat.search_chatrooms(name=name)
    return df[0]['UserName']

groups.append(group_id(u'库有引力'))
groups.append(group_id(u'大北湖幸福快乐的家'))
groups.append(group_id(u'早睡早起方能养生'))
#groups.append(group_id(u'小伙伴们'))

mygirl = itchat.search_friends(name=u'我方水晶')[0]['UserName']

# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    if msg['FromUserName'] == mygirl:
        if u'老公' in msg['Text']:
            itchat.send(u'媳妇，有何吩咐！', mygirl)
    else:
        friend = itchat.search_friends(userName=msg['FromUserName'])
        friend_name = friend['RemarkName']
        print('%s said: %s' % (friend_name, msg['Text']))
        itchat.send('%s' % tuling(msg['Text']),msg['FromUserName'])

'''
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
'''
@itchat.msg_register([TEXT], isGroupChat=True)
def group_text_reply(msg):
    item = msg['FromUserName']
    if item in groups:
        itchat.send(u'%s' % tuling(msg['Text']), item)

itchat.run()
