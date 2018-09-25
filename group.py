#coding=utf-8
import itchat
from itchat.content import TEXT
from itchat.content import *

@itchat.msg_register(TEXT, isGroupChat=True)
def group_text(msg):
    group  = itchat.get_chatrooms(update=True)
    from_user = ''
    for g in group:
        if g['NickName'] == 'hhh':#从群中找到指定的群聊
            from_group = g['UserName']
            for menb in g['MemberList']:
                #print(menb['NickName'])
                if menb['NickName'] == "hhh":#从群成员列表找到用户,只转发他的消息
                    from_user = menb['UserName']
                    break
        if g['NickName'] == 'qqq':#把消息发到这个群
            to_group = g['UserName']
    if msg['FromUserName'] == from_group:
        if msg['ActualUserName'] == from_user:
            itchat.send('%s:%s'%(msg['ActualNickName'],msg['Content']),to_group)
itchat.auto_login(hotReload=False)
itchat.run()