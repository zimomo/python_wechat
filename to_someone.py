#coding=utf8
import itchat

from itchat.content 
import *
 
 
gname = '狗年旺德福'
context = '祝大家国庆快乐（测试消息）'

def SendChatRoomsMsg(gname, context):
    # 获取群组所有的相关信息（注意最好群聊保存到通讯录）
    myroom = itchat.get_chatrooms(update=True)
    # myroom = itchat.get_chatrooms()
    #定义全局变量（也可以不定义）
    global username
    # 传入指定群名进行搜索，之所以搜索，是因为群员的名称信息也在里面
    myroom = itchat.search_chatrooms(name=gname)
    for room in myroom:
        # print(room)
        #遍历所有NickName为键值的信息进行匹配群名
        if room['NickName'] == gname:
           username = room['UserName']
            # 得到群名的唯一标识，进行信息发送
           itchat.send_msg(context, username)
        else:
           print('No groups found')



if __name__ == '__main__':
    itchat.auto_login()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()