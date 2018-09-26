#coding=utf8
from wxpy import *
bot = Bot(cache_path=True)

# 机器人账号自身
myself = bot.self

# 向文件传输助手发送消息
bot.file_helper.send('Hello from wxpy!')