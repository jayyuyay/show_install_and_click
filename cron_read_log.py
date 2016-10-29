#! /usr/bin/python
# -*- coding: utf-8 -*-
# auth:yujie(libai)
# date:20160105
# desc:分析click和install日志数据
# 根据时间，下游，offer_id,国家码分类统计

import os
from datetime import date
from datetime import timedelta
import MySQLdb
import glob

def click_scan_storage():
    # today = date.today()
    # yestoday = today - timedelta(days=1)
    # click_log_path = './solo-ad-data/leadhug/click/%s/' % yestoday.strftime("%Y%m%d")
    click_log_path = '/home/jay/PycharmProjects/show_click_and_install/solo-ad-data/leadhug/click/%s/' % '20151230'  # test
    if not os.path.exists(click_log_path):
        print "not exists"
        return
    if not os.path.isdir(click_log_path):
        print "not a dir"
        return
    for root, dirs, files in os.walk(click_log_path, topdown=False):
        files.sort()
        value = {}
        for file in files:
            path = click_log_path + file
            with open(path, 'r') as fd:
                for line in fd:
                    cli = line.split("|")
                    date = cli[0][:13]
                    aff = cli[6]
                    offer_id = cli[7]
                    if "&" in cli[9]:
                        country = cli[9].split("&")[1]
                    else:
                        country = cli[9]
                    add_all_click = "|".join([date, aff, offer_id, country])
                    if add_all_click in value:
                        value[add_all_click] += 1
                    else:
                        value[add_all_click] = 1
        record_l = []
        for key in value:
            click = value[key]
            record = key.split("|")
            create_time = "-".join(record[0].split(":"))
            record_l.append((create_time,record[1],record[2],record[3],click))
        sql = "insert into cli_and_ins(create_time,aff,offer_id,country_code,click) values (%s,%s,%s,%s,%s)"
        cursor.executemany(sql,record_l)
        conn.commit()


def install_scan_storage():

    # today = date.today()
    # yestoday = today - timedelta(days=1)
    # filename = yestoday.strftime("%Y-%m-%d")
    # install_log_path = './solo-ad-data/leadhug/install/%s' % filename
    install_log_path = '/home/jay/PycharmProjects/show_click_and_install/solo-ad-data/leadhug/install/%s' % "2015-12-30"

    file = glob.glob(install_log_path+'*')
    value = {}
    with open(file[0],"r") as fd:
        for line in fd:

            cli = line.split("|")
            date = cli[0][:13]
            aff = cli[1]
            offer_id = cli[2]
            if "&" in cli[4]:
                country = cli[4].split("&")[1]
            else:
                country = cli[4]
            add_all_install = "|".join([date, aff, offer_id, country])

            if add_all_install in value:
                value[add_all_install] += 1
            else:
                value[add_all_install] = 1
    record_l = []
    for key in value:
        install = value[key]
        record = key.split("|")
        create_time = "-".join(record[0].split(":"))
        record_l.append((install,create_time,record[1],record[2],record[3]))
    sql = "update cli_and_ins set install=%s where create_time=%s and aff=%s and offer_id=%s and country_code=%s"
    cursor.executemany(sql,record_l)
    conn.commit()


if __name__ == "__main__":
    conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="cli_and_ins", charset="utf8")
    cursor = conn.cursor()
    click_scan_storage()
    install_scan_storage()
    cursor.close()
    conn.close()