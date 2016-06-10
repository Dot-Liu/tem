#!/usr/bin/python
#-*- coding: utf8 -*-

import web

from route import route
from database import *
from output import output
from encrypt import *

@route('/api/user/is/login')
class IsLogin:
    def POST(self):
        return IsLogin.getLoginInfo()
    def GET(self):
        return IsLogin.getLoginInfo()

    @staticmethod
    def getLoginInfo():
        session = web.ctx.session
        is_login = True if session.has_key('user_id') else False
        if is_login:
            type = session['user_type']
        else:
            type = None

        return output(200, {'type':type, 'is_login':is_login})


