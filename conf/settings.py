#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

APPLICATION_ENV = os.getenv("APPLICATION_ENV")

"""Log Setting
"""
MAPPING = {"CRITICAL": 50,
           "ERROR": 40,
           "WARNING": 30,
           "INFO": 20,
           "DEBUG": 10,
           "NOTSET": 0,
           }

# 日志路径
LOGGER_FILE_PATH = "/opt/logs/shield/{0}.log"

# 写入文件的日志等级，由于是详细信息，推荐设为debug
FILE_LOG_LEVEL = "DEBUG"
# 控制台的日照等级，info和warning都可以，可以按实际要求定制
CONSOLE_LOG_LEVEL = "INFO"
# 缓存日志等级，最好设为error或者critical
MEMOEY_LOG_LEVEL = "ERROR"
# 致命错误等级
URGENT_LOG_LEVEL = "CRITICAL"
# 缓存溢出后的邮件标题
ERROR_THRESHOLD_ACHEIVED_MAIL_SUBJECT = "Too many errors occurred during the execution"
# 缓存溢出的阀值
ERROR_MESSAGE_THRESHOLD = 50
# 致命错误发生后的邮件标题
CRITICAL_ERROR_ACHEIVED_MAIL_SUBJECT = "Fatal error occurred"

"""Redis Settings
"""
redis_server = {
    "develop": {
        "shield": {
            "host": "127.0.0.1",
            "port": 6379,
            "db": 0,
            "password": ""
        }
    },
    "production": {
        "shield": {
            "host": "127.0.0.1",
            "port": 7299,
            "db": 0,
            "password": "6BwXQsFN8ZE2Z5SLVPg8w4AQG"
        }
    }
}

redis_queue = {
    "shield": {
        "queueShieldPack": "shield_queue_deploy_pack",
        "queueShieldCode": "shield_queue_shield_code"
    }
}

redis_hash = {
    "shield": {
    }
}

redis_set = {
    "shield": {
    }
}

"""MySQL Settings
"""
mysql_server = {
    "develop": {
        "shield": {
            "host": "192.168.1.112",
            "port": 3306,
            "user": "shield_admin",
            "passwd": "nqjFV%oxasdha1122",
            "db": "shield_admin",
            "use_unicode": True,
            "charset": "utf8"
        }
    },
    "production": {
        "shield": {
            "host": "172.21.0.10",
            "port": 10627,
            "user": "shield",
            "passwd": "QD@Ov2Z5SLFqjFV%",
            "db": "shield_admin",
            "use_unicode": True,
            "charset": "utf8"
        }
    }
}

mysql_tables = {
    "shield": {
        "Url": "shield_url",
        "Partner": "shield_partner",
        "Port": "shield_port",
        "SnapShot": "shield_url_snapshot_log",
        "shieldCode": "shield_visit",
        "shieldCodeHistory": "shield_visit_history",
        "urlCheckLog": "shield_url_check_log"
    }
}

"""
Mail Settings
"""
MAIL_HOST = "smtp.exmail.qq.com"
MAIL_PORT = 465
MAIL_USER = "notification@360huitong.com"
MAIL_PWD = "bkjftA23NhJC"
MAIL_FROM = "notification@360huitong.com"
MAIL_TO = ["yhk@360huitong.com", "liuwei@360huitong.com", "chenyuan@360huitong.com"]

"""
Shield ScreenShot Setting
"""
SHIELD_PHANTOMJS_PATH = "/bin/phantomjs"
SHIELD_PIC_PATH = "/opt/cafe/bidding/shield_admin/public/uploads/"

"""
Shield Deploy Setting
"""
SHIELD_DEPLOY_PUBLIC_PATH = "/opt/cafe/bidding/shield_admin/public/uploads/deploy_pack"
SHIELD_DEPLOY_PACK_PATH = "/opt/cafe/bidding/shield_deploy_pack"
SHIELD_DEPLOY_SOURCE_PATH = "/opt/cafe/bidding/shield_deploy_source"

