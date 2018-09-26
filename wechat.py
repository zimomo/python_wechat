#coding=utf8
from wxpy import *
import time
from __future__ import unicode_literals
bot = Bot(console_qr=True, cache_path=True)
# 机器人账号自身
while True:
		myself = bot.self
		# 查找昵称为'乙醚。'的好友
		#my_friend = bot.friends().search(u'小小世界')[0]
		my_group = bot.groups().search(u'hhh')[0]
		print(my_group)
		#my_friend.send('Hello, WeChat!')
		content = '我爱北京天安门';
		my_group.send(content)
		#休眠十秒
		time.sleep(60)
		# 向文件传输助手发送消息
		#bot.file_helper.send('Hello from wxpy!')