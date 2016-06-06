#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# maximal used disk space in percent
DSPACEPERCENT = 80
# Percent in decimal to minimize the difference between this program and df -h
# 1.01 = 1 Percent
# 1.10 = 10 Percent
PERCENT_DEC = 1.01

# Mailserver settings
EMAIL_SENDER = "root"
EMAIL_RECIPIENT = "guenter"
EMAIL_LINK = ""
SMTPSERVER = "127.0.0.1"
SMTP_SSL = True
USE_AUTH = True
SMTPUSER = ""
SMTPPASSWORD = ""
SMTP_PORT = 465