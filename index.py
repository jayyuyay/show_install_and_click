#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from pprint import pprint

define("port", default=8000, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="log database host")
define("mysql_database", default="cli_and_ins", help="log database name")
define("mysql_user", default="root", help="log database user")
define("mysql_password", default="1234", help="blog database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            title="cli_and_ins",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url="/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class IndexHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        sql = "select distinct aff from cli_and_ins"
        affs = self.db.query(sql)
        sql = "select distinct offer_id from cli_and_ins"
        offers = self.db.query(sql)
        sql = "select distinct country_code from cli_and_ins"
        countrys = self.db.query(sql)
        records = []
        self.render("index.html", affs=affs, offers=offers, countrys=countrys, records=records, click=0, install=0,conversion=0)

    def post(self):
        sql = "select distinct aff from cli_and_ins"
        aff = self.db.query(sql)
        sql = "select distinct offer_id from cli_and_ins"
        offer = self.db.query(sql)
        sql = "select distinct country_code from cli_and_ins"
        country = self.db.query(sql)
        query = "select create_time,aff,offer_id,country_code,click,install from cli_and_ins where "
        time = self.get_argument('time')
        query = query + "create_time like '%%{0}%%'".format(time)
        affs = self.get_arguments('aff')
        if affs:
            aff_l = ["aff like '%%{0}%%'".format(a) for a in affs]
            query = query + " and " + "("+" or ".join(aff_l)+")"
        else:
            query = query + " and " + "aff like '%%%%'"
        offer_ids = self.get_arguments('offer_id')
        if offer_ids:
            offer_l = ["offer_id like '%%{0}%%'".format(o) for o in offer_ids]
            query = query + " and " + "(" + " or ".join(offer_l) + ")"
        else:
            query = query + " and " + "offer_id like '%%%%'"
        countrys = self.get_arguments('country')
        if countrys:
            country_l = ["country_code like '%%{0}%%'".format(c) for c in countrys]
            query = query + " and " + "(" + " or ".join(country_l) + ")"
        else:
            query = query + " and " + "country_code like '%%%%'"
        records = self.db.query(query)
        click = 0
        install = 0
        for record in records:
            click += record['click']
            install += record['install']
        if click != 0:
            self.render("index.html", affs=aff, offers=offer, countrys=country, records=records,
                        click=click, install=install, conversion=round(float(install)/float(click), 2))
        else:
            self.render("index.html", affs=aff, offers=offer, countrys=country, records=records,
                        click=0, install=0, conversion=0)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
