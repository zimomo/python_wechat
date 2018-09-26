# coding=utf-8
import schedule
from wxpy import *
import  json
import requests
from urllib.parse import urlencode
from datetime import datetime
import time
 
bot=Bot(cache_path=True) #Windows上登陆网页微信，并保存登陆状态
#bot=Bot(cache_path=True,console_qr=2) #Linux服务器终端界面上使用：
# WEATHER_KEY = 'XXXXX'  # 这里填拿到的图灵机器人key
# HUANGLI_KEY = "XXXXX"  #这里填写拿到的老黄历key
# def get_weather():
#     apiUrl = 'http://www.tuling123.com/openapi/api'
#     data = {
#         'key': WEATHER_KEY,
#         'info': '北京今天天气', #这里换成你自己所在城市
#     }
#     try:
#         r = requests.post(apiUrl, data=data).json()
#         weather=r.get('text').split(':')[1]
#         return "北京今日天气："+weather+"\n"
#     except:
#         return "查询天气信息失败\n"
 
# def get_huangli():
#     data = {}
#     data["appkey"] = HUANGLI_KEY
#     data["year"] = datetime.now().year
#     data["month"] = datetime.now().month
#     data["day"] = datetime.now().day
#     url_values = urlencode(data)
#     url = "http://api.jisuapi.com/huangli/date" + "?" + url_values
#     r = requests.get(url)
#     jsonarr = json.loads(r.text)
#     if jsonarr["status"] != u"0":
#         print(jsonarr["msg"])
#         return "今日无黄历信息"
#     result = jsonarr["result"]
#     content1='天干地支:' + ','.join(result['suici'])
#     content2='今日应当注意的生肖:' + result["chong"]
#     content3='宜：' + ','.join(result['yi'])
#     content4='忌：' + ','.join(result['ji'])
#     return '今日黄历：'+content1+'\n'+content2+'\n'+content3+'\n'+content4+"\n"
 
def get_everydayWords():
    url = 'http://open.iciba.com/dsapi/'
    r =requests.get(url)
    content = json.loads(r.text)
    return '每日一句：\n'+content['content'] +'\n'+content['note']+"\n"
 
def get_context():
    return "美好的一天从我的问候开始:各位早上好!\n"+get_weather()+get_huangli()+get_everydayWords()+"发送信息时间："+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 
def SentChatRoomsMsg(name, context):
    my_group = bot.groups().search(name)[0]
    my_group.send(context)
 
def job():
    group_list = ['hhh','狗年旺德福','噢你个biang彪子']  #这里填写群名字,可以发送至多个群
    content = get_context()
    for group_name in group_list:
        SentChatRoomsMsg(group_name, content)
        print('sended msg to ' + group_name +"\n"+ " content: " + content+"\n")
 
schedule.every().day.at("7:30").do(job)
while True:
    schedule.run_pending()#确保schedule一直运行
    time.sleep(1)
bot.join() #保证上述代码持续运行
 
 
 
