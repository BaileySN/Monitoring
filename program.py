#!/usr/bin/env python3
# -*- coding: utf-8
# https://github.com/giampaolo/psutil/blob/master/scripts/disk_usage.py
import sys
import os
import psutil
from conf import DSPACEPERCENT
from bin import mailsend


def testmail(msg):
    mailsend.emailsend(msg)
    print("sending Testmail...")


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
    if int(usage.percent) > int(DSPACEPERCENT):
        return float(usage.percent)
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


def main():

    send = 0
    report = []
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    report.append(templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount")+"\n")
    print(templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount"))

    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue

        df = disk_space_percent(part.mountpoint)

        if df != float(200):
            send += 1
            print("Partition fast voll: "+part.device+" Mountpoint: "+part.mountpoint+" ist "+str(df)+"% voll")
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
                part.mountpoint)+"\n")


    if send != 0:
        mailsend.emailsend(report)

    print("Fertig")


if __name__ == '__main__':
    sys.exit(main())
