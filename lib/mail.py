#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Mail类
"""

import logging
import logging.handlers
import smtplib
import time
import json
from conf.settings import *
from email.mime.text import MIMEText


class OptmizedMemoryHandler(logging.handlers.MemoryHandler):
    """
    由于自带的MemoryHandler达到阀值后，每一条缓存信息会单独处理一次，这样如果阀值设的100，
    会发出100封邮件，这不是我们希望看到的，所以这里重写了memoryHandler的2个方法，
    当达到阀值后，把缓存的错误信息通过一封邮件发出去.
    """

    def __init__(self, capacity, mail_subject):
        logging.handlers.MemoryHandler.__init__(self, capacity, flushLevel=logging.ERROR, target=None)
        self.mail_subject = mail_subject
        self.flushed_buffers = []

    def shouldFlush(self, record):
        """
        检查是否溢出
        """
        if len(self.buffer) >= self.capacity:
            return True
        else:
            return False

    def flush(self):
        """
        缓存溢出时的操作，
        1.发送邮件 2.清空缓存 3.把溢出的缓存存到另一个列表中，方便程序结束的时候读取所有错误并生成报告
        """
        if self.buffer != [] and len(self.buffer) >= self.capacity:
            content = ""
            for record in self.buffer:
                message = record.getMessage()
                level = record.levelname
                ctime = record.created
                t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
                content += t + " " + "*" + level + "* : " + message + "\n"
            self.mailnotification(self.mail_subject, content)
            self.flushed_buffers.extend(self.buffer)
            self.buffer = []

    @staticmethod
    def mailnotification(subject, content):
        """
        发邮件的方法
        """
        msg = MIMEText(content, "plain", "UTF-8")
        msg['Subject'] = subject
        msg['From'] = MAIL_FROM
        msg['To'] = ";".join(MAIL_TO)
        try:
            s = smtplib.SMTP_SSL(host=MAIL_HOST, port=MAIL_PORT)
            s.ehlo()
            s.login(MAIL_USER, MAIL_PWD)
            s.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
            s.close()
        except smtplib.SMTPException, e:
            print "send mail error:{0}".format(e)
