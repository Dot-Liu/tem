#!/usr/bin/python
#-*- coding: utf8 -*-

import web

from route import route
from output import *

@route('/api/user/logout')
class UserLogout:
    def GET(self):
        return UserLogout.logout(web.ctx.session)
    def POST(self):
        return UserLogout.logout(web.ctx.session)

    @staticmethod
    def logout(session):
        if session.has_key('user_id'):
            session.kill()
            return output(200)
        else:
            return output(411)