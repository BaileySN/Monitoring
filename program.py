#!/usr/bin/env python3
# -*- coding: utf-8
#############################################################################
# Monitoring  https://github.com/BaileySN/Monitoring                        #
# Copyright (C) 2016  Bailey-Solution                                       #
#                                                                           #
# This program is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by      #
# the Free Software Foundation, either version 3 of the License, or         #
# (at your option) any later version.                                       #
#                                                                           #
# This program is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
# GNU General Public License for more details.                              #
#                                                                           #
# You should have received a copy of the GNU General Public License         #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#############################################################################

import sys
import os
import psutil
from conf import DSPACEPERCENT, PERCENT_DEC
from bin import mailsend
from optparse import OptionParser
__version__ = "0.5a"


def testmail(msg):
    print("sending Testmail...")
    mailsend.emailsend(msg)


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def disk_space_percent(path):
    usage = psutil.disk_usage(path)
    psf = float(usage.percent) * float(PERCENT_DEC)
    if int(psf) > int(DSPACEPERCENT):
        return '%3.2f' %(psf)
    else:
        return float(200)


def disk_usage(method, path):
    usage = psutil.disk_usage(path)
    if method == "total":
        var = bytes2human(usage.total)
    elif method == "free":
        var = bytes2human(usage.free)
    else:
        var = bytes2human(usage.used)
    return var


def df_check():

    send = 0
    report = []
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    report.append(templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount")+"<br />")
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount"))

    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue

        df = disk_space_percent(part.mountpoint)

        if df != float(200):
            send += 1
            # print("Partition fast voll: "+part.device+" Mountpoint: "+part.mountpoint+" ist "+str(df)+"% voll")
            print(templ % (
                part.device,
                disk_usage("total", part.mountpoint),
                disk_usage("used", part.mountpoint),
                disk_usage("free", part.mountpoint),
                float(df),
                part.fstype,
                part.mountpoint))

            report.append(templ % (
                part.device,
                disk_usage("total", part.mountpoint),
                disk_usage("used", part.mountpoint),
                disk_usage("free", part.mountpoint),
                float(df),
                part.fstype,
                part.mountpoint)+"<br />")

    if send != 0:
        mailsend.emailsend(report)

    # print("Finish")

def df_report():

    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount"))

    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue

        df = disk_space_percent(part.mountpoint)

        if df != float(200):
            print(templ % (
                part.device,
                disk_usage("total", part.mountpoint),
                disk_usage("used", part.mountpoint),
                disk_usage("free", part.mountpoint),
                float(df),
                part.fstype,
                part.mountpoint))

def main():
    usage = "HDD Space Monitoring v%s" %(__version__)
    parser = OptionParser(usage=usage)
    parser.add_option("--testmail", action="store_true", default=False,
                      dest="testmail", help="Sending Testmail.")
    parser.add_option("--df_check", action="store_true", default=False,
                      dest="df_check", help="check disk usage and send mail if goes over %s%%" %(DSPACEPERCENT))
    parser.add_option("--report", action="store_true", default=False,
                      dest="report", help="check disk usage and print if goes over %s%%" %(DSPACEPERCENT))
    (options, args) = parser.parse_args()

    if options.testmail:
        testmail("This is a test Report, for checking the Mail Settings.")
        exit(2)
    elif options.report:
        df_report()
        exit(2)
    else:
        df_check()
        exit(2)


if __name__ == '__main__':
    sys.exit(main())
