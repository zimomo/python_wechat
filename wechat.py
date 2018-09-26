#coding=utf8
from __future__ import unicode_literals
from wxpy import *
import time
bot = Bot()
print bot, type(bot)
# 机器人账号自身
while True:
		if bot is not None:
			print bot, type(bot)
			myself = bot.self
			# 查找昵称为'乙醚。'的好友
			#my_friend = bot.friends().search(u'小小世界')[0]
			# try:
			# 	my_group = bot.groups().search(u'狗年旺德福')[0]
			# except:
			# 	bot = Bot(console_qr=True, cache_path=True)
			# 	my_group = bot.groups().search(u'狗年旺德福')[0]
			my_group = bot.groups().search(u'狗年旺德福')[0]	
			print my_group, type(my_group)
			print(my_group)
			#my_friend.send('Hello, WeChat!')
			content = '我爱北京天安门';
			my_group.send(content)
			#休眠十秒
			time.sleep(10)
			# 向文件传输助手发送消息
			#bot.file_helper.send('Hello from wxpy!')
		else:
			bot = Bot(console_qr=True, cache_path=True)