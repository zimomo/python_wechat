#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Log类
"""

import json
import logging
import logging.handlers

from conf.settings import *
from lib import OptmizedMemoryHandler

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SSLSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            from email.utils import formatdate
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr,
                ";".join(self.toaddrs),
                self.getSubject(record),
                formatdate(), msg)
            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class MyLogger:
    """
    my_logger的配置
    """

    def __init__(self, log_file, file_level, console_level, memory_level, urgent_level):
        self.config(log_file, file_level, console_level, memory_level, urgent_level)

    def config(self, log_file, file_level, console_level, memory_level, urgent_level):
        # 生成root my_logger
        self.my_logger = logging.getLogger("crawler")
        self.my_logger.setLevel(MAPPING[file_level])

        # 生成RotatingFileHandler，设置文件大小为10M,编码为utf-8，最大文件个数为100个，如果日志文件超过100，则会覆盖最早的日志
        # self.fh = logging.handlers.RotatingFileHandler(log_file, mode='a', maxBytes=1024 * 1024 * 10, backupCount=100,
        #                                                encoding="utf-8")
        # self.fh.setLevel(MAPPING[file_level])
        self.fh = logging.handlers.TimedRotatingFileHandler(log_file, "D", 1, 30)
        self.fh.suffix = "%Y%m%d.log"
        self.fh.setLevel(MAPPING[file_level])

        # 生成StreamHandler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(MAPPING[console_level])

        # 生成优化过的MemoryHandler,ERROR_MESSAGE_THRESHOLD是错误日志条数的阀值
        self.mh = OptmizedMemoryHandler(ERROR_MESSAGE_THRESHOLD, ERROR_THRESHOLD_ACHEIVED_MAIL_SUBJECT)
        self.mh.setLevel(MAPPING[memory_level])

        # 生成SMTPHandler
        self.sh = SSLSMTPHandler(mailhost=(MAIL_HOST, MAIL_PORT), fromaddr=MAIL_FROM,
                                 toaddrs=MAIL_TO,
                                 subject=CRITICAL_ERROR_ACHEIVED_MAIL_SUBJECT,
                                 credentials=(MAIL_USER, MAIL_PWD))
        self.sh.setLevel(MAPPING[urgent_level])

        # 设置格式
        formatter = logging.Formatter("%(asctime)s *%(levelname)s* : %(msg)s", '%Y-%m-%d %H:%M:%S')
        self.ch.setFormatter(formatter)
        self.fh.setFormatter(formatter)
        self.mh.setFormatter(formatter)
        self.sh.setFormatter(formatter)

        # 把所有的handler添加到root my_logger中
        self.my_logger.addHandler(self.ch)
        self.my_logger.addHandler(self.fh)
        self.my_logger.addHandler(self.mh)
        self.my_logger.addHandler(self.sh)

    def debug(self, msg):
        # if isinstance(msg, str):
        #     msg = json.dumps(msg, encoding="UTF-8", ensure_ascii=False)
        # elif isinstance(msg, tuple):
        #     tmp_msg = list(msg)
        #     msg = json.dumps(tmp_msg, encoding="UTF-8", ensure_ascii=False)
        # else:
        #     msg = msg.encode("UTF-8")
        self.my_logger.debug(msg)

    def info(self, msg):
        # if isinstance(msg, str):
        #     msg = json.dumps(msg, encoding="UTF-8", ensure_ascii=False)
        # elif isinstance(msg, tuple):
        #     tmp_msg = list(msg)
        #     msg = json.dumps(tmp_msg, encoding="UTF-8", ensure_ascii=False)
        # else:
        #     msg = msg.encode("UTF-8")
        self.my_logger.info(msg)

    def warning(self, msg):
        # if isinstance(msg, str):
        #     msg = json.dumps(msg, encoding="UTF-8", ensure_ascii=False)
        # elif isinstance(msg, tuple):
        #     tmp_msg = list(msg)
        #     msg = json.dumps(tmp_msg, encoding="UTF-8", ensure_ascii=False)
        # else:
        #     msg = msg.encode("UTF-8")
        self.my_logger.warning(msg)

    def error(self, msg):
        # if isinstance(msg, str):
        #     msg = json.dumps(msg, encoding="UTF-8", ensure_ascii=False)
        # elif isinstance(msg, tuple):
        #     tmp_msg = list(msg)
        #     msg = json.dumps(tmp_msg, encoding="UTF-8", ensure_ascii=False)
        # else:
        #     msg = msg.encode("UTF-8")
        self.my_logger.error(msg)

    def critical(self, msg):
        # if isinstance(msg, str):
        #     msg = json.dumps(msg, encoding="UTF-8", ensure_ascii=False)
        # elif isinstance(msg, tuple):
        #     tmp_msg = list(msg)
        #     msg = json.dumps(tmp_msg, encoding="UTF-8", ensure_ascii=False)
        # else:
        #     msg = msg.encode("UTF-8")
        self.my_logger.critical(msg)
