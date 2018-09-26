#coding=utf8
from wxpy import *
import time
bot = Bot(console_qr=True, cache_path=True)

print(bot)
# 机器人账号自身
while True:
	if bot is not None:
		myself = bot.self
		# 查找昵称为'乙醚。'的好友
		#my_friend = bot.friends().search(u'小小世界')[0]
		my_group = bot.groups().search(u'狗年旺德福')[0]

		#my_friend.send('Hello, WeChat!')
		my_group.send('我爱北京天安门')
		#休眠十秒
		time.sleep(60)
		# 向文件传输助手发送消息
		#bot.file_helper.send('Hello from wxpy!')
	else:
		bot = Bot(console_qr=True, cache_path=True)