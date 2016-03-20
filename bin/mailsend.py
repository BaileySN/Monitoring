#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from conf import EMAIL_RECIPIENT, EMAIL_SENDER, SMTPSERVER, SMTPUSER, SMTPPASSWORD, DSPACEPERCENT
from bin import hostinfo


hostname = hostinfo.hostn()
ipaddr = hostinfo.hostaddr()


class emailsend(object):
    def __init__(self, report):
        self.txt = "text"


    def __new__(self, report):
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = ("Achtung: Platte am Server "+hostname+" ueber "+str(DSPACEPERCENT)+"% voll")
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT

        # Create the body of the message (a plain-text and an HTML version).
        text = "Platte am Server %s ist ueber %s%% voll.\n Adresse: %s \n Info: %s" %(hostname, str(DSPACEPERCENT), ipaddr, report)
        html = """
<html>
<head></head>
<body>
<p>Platte am Server %s ist ueber <span style="color:red">%s%%</span> voll.<br />
Adresse: %s<br />
Info:<br />
%s
</p>
</body>
</html>""" %(hostname, str(DSPACEPERCENT), ipaddr, report)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        s = smtplib.SMTP(SMTPSERVER)
        s.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        s.quit()
