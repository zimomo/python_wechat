#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
实时收集屏蔽警告数据并推送至指定微信群
"""
from __future__ import unicode_literals
from conf.settings import *
from wxpy import *
import os
import sys

import time
import redis

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

reload(sys)
sys.setdefaultencoding('utf8')



bot = Bot(console_qr=True)
shield_redis = redis.StrictRedis(host=redis_server[APPLICATION_ENV]["shield"]["host"],
                                      port=redis_server[APPLICATION_ENV]["shield"]["port"],
                                      password=redis_server[APPLICATION_ENV]["shield"]["password"])
print bot, type(bot)
print(shield_redis)
#my_group = bot.groups().search(u'(内)落地页屏蔽预警群')[0]
#content = '我爱北京天安门';
#my_group.sen d(content)
# 机器人账号自身
while True:
	if shield_redis is not None:
		print bot, type(bot)
		myself = bot.selfs
		# 查找昵称为'乙醚。'的好友
		#my_friend = bot.friends().search(u'小小世界')[0]
		try:
			my_group = bot.groups().search(u'(内)落地页屏蔽预警群')[0]
		except:
			bot = Bot(console_qr=True, cache_path=True)
			#bot = Bot(console_qr=2,cache_path=True)
			my_group = bot.groups().search(u'(内)落地页屏蔽预警群')[0]
		#my_group = bot.groups().search(u'(内)落地页屏蔽预警群')[0]	
		print my_group, type(my_group)
		print(my_group)

		_queue_shield_wechat = shield_redis.blpop(redis_queue['shield']['queueShieldWechat'], 0)[1]
		print(_queue_shield_wechat)
		print len (_queue_shield_wechat)
		#my_friend.send('Hello, WeChat!')
		if len(_queue_shield_wechat) > 0:
		#content = '住进布达拉宫，\n我是雪域最大的王。\n流浪在拉萨街头，\n我是世间最美的情郎。'
			my_group.send(_queue_shield_wechat)
		#休眠十秒
		time.sleep(10)
		# 向文件传输助手发送消息
		#bot.file_helper.send('Hello from wxpy!')
	else:
		print('ceshi')
		shield_redis = redis.StrictRedis(host=redis_server[APPLICATION_ENV]["shield"]["host"],
                                              port=redis_server[APPLICATION_ENV]["shield"]["port"],
                                              password=redis_server[APPLICATION_ENV]["shield"]["password"])