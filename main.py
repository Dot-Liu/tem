#!/usr/bin/env python
# -*- coding: utf8 -*-

import web
import consts
import route
import cgi
import sites

app = web.application(route.getURLs(), globals())
# db = web.database(dbn = 'mysql', db = 'test', user = 'root', pw = '123456')
# store = web.session.DBStore(db, 'sessions')
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store)

def session_hook():
    web.ctx.session = session
app.add_processor(web.loadhook(session_hook))

if __name__ == "__main__":
    cgi.maxlen = 10 * 1024 * 1024
    # web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
