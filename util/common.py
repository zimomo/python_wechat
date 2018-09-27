#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
通用工具集
"""

import time
import datetime
import socket
import httplib2
import uuid
import hashlib

from conf.settings import *
from dateutil import rrule
from functools import wraps

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

from PIL import Image
from PIL import ImageChops


def getmonths(start_date, end_date):
    """
    获取两个日期之间的月份数
    :param start_date:
    :param end_date:
    :return:
    """
    months = rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date).count()
    year = months / 12
    month = months % 12

    return year, month


def retry(myexception, tries=4, delay=3, backoff=2):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except socket.timeout as ex:
                    msg = "%s, Retrying in %d seconds..." % (str(ex), mdelay)
                    log_system.info(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
                except myexception as ex:
                    msg = "%s, Retrying in %d seconds..." % (str(ex), mdelay)
                    log_system.info(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return str(ex)

        return f_retry

    return deco_retry


@retry(Exception)
def do_http(_method, _url, _cookie, _body):
    """
    do http request
    :param _cookie:
    :param _method:
    :param _url:
    :param _body:
    :return:
    """
    _timeout = 3
    h = httplib2.Http(timeout=_timeout, disable_ssl_certificate_validation=True)
    _headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': _cookie
    }

    if _method == "POST":
        resp, content = h.request(
            uri=_url,
            method='POST',
            headers=_headers,
            body=_body
        )
    else:
        resp, content = h.request(
            uri=_url,
            method='GET',
            headers=_headers
        )

    return resp["status"], content.decode('utf-8')


def convert_n_bytes(n, b):
    bits = b * 8
    return (n + 2 ** (bits - 1)) % 2 ** bits - 2 ** (bits - 1)


def convert_4_bytes(n):
    return convert_n_bytes(n, 6)


def get_hash_code():
    s = str(uuid.uuid1())
    h = 0
    n = len(s)
    for i, c in enumerate(s):
        h += ord(c) * 31 ** (n - 1 - i)
    hashcode = convert_4_bytes(h)
    if hashcode < 0:
        hashcode = -hashcode

    return "%016d" % hashcode


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


def query_send_detail(biz_id, phone_number, page_size, current_page, send_date):
    queryRequest = QuerySendDetailsRequest.QuerySendDetailsRequest()
    # 查询的手机号码
    queryRequest.set_PhoneNumber(phone_number)
    # 可选 - 流水号
    queryRequest.set_BizId(biz_id)
    # 必填 - 发送日期 支持30天内记录查询，格式yyyyMMdd
    queryRequest.set_SendDate(send_date)
    # 必填-当前页码从1开始计数
    queryRequest.set_CurrentPage(current_page)
    # 必填-页大小
    queryRequest.set_PageSize(page_size)

    # 调用短信记录查询接口，返回json
    queryResponse = acs_client.do_action_with_exception(queryRequest)

    # TODO 业务处理

    return queryResponse


def get_time_zero_clock_of_today():
    """
    取得当天0点的时间戳,返回的是Long型的数据
    :return: long
    """
    zero_time = time.mktime(
        time.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time())), '%Y-%m-%d %H:%M:%S'))

    return long(zero_time)


def get_day_nday_ago(n):
    """
    获取n天前的日期
    :param n:
    :return:
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    t = time.strptime(today, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]


def send_mail(_subject, _content):
    """
    邮件发送
    :param _subject:
    :param _content:
    :return:
    """
    smtp = SMTP_SSL(MAIL_HOST)

    smtp.ehlo(MAIL_HOST)
    smtp.login(MAIL_USER, MAIL_PWD)

    msg = MIMEText(_content, "plain", "UTF-8")
    msg["Subject"] = Header(_subject, "UTF-8")
    msg["from"] = MAIL_FROM
    msg["to"] = ";".join(MAIL_TO)

    smtp.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())

    smtp.quit()


def get_file_md5(filename):
    """
    获取指定文件的MD5值
    :param filename:
    :return:
    """
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def compare_images(path_one, path_two, diff_save_location):
    """
    比较图片，如果有不同则生成展示不同的图片
    @参数一: path_one: 第一张图片的路径
    @参数二: path_two: 第二张图片的路径
    @参数三: diff_save_location: 不同图的保存路径
    """

    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
    diff = ImageChops.difference(image_one, image_two)
    if diff.getbbox() is None:
        # 图片间没有任何不同则直接退出
        return
    else:
        diff.save(diff_save_location)
