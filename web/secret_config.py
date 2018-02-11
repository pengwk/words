# _*_ coding:utf-8 _*_
# python2.7

import os

config = {
    "DATABASE_URL": "",
    "MAIL_USERNAME": "handsome_boy@pengwk.com",
    "MAIL_PASSWORD": "",
    "MAIL_DEFAULT_SENDER": '"handsome_boy" <handsome_boy@pengwk.com>',
    "MAIL_SERVER":  "smtp.exmail.qq.com",
    "MAIL_PORT": "465",
}

for key, value in config.items():
    os.environ[key] = value