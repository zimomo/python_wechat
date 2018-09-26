#coding=utf8
import itchat
itchat.auto_login()
users=itchat.search_friends("小小世界")
print(users)
userName= users[0]['NickName']
print(userName)
#itchat.send('你好冰糖葫芦娃哈哈~',toUserName=userName)

