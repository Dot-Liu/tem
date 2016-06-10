#!/usr/bin/python
#-*- coding: utf8 -*-

import web

from route import route
from database import *
from output import output
from encrypt import *

@route('/api/user/login')
class UserLogin:
    def POST(self):
        input = web.input(login_name = None, password = None)
        if input.login_name == None or input.password == None:
            return output(110)

        db = getDb()
        results = db.select('user', vars = {'login_name':input.login_name}, where = "login_name=$login_name")
        if len(results) == 0:
            return output(422)
        user = results[0]
        if user.type == '2':
            return output(422)
        if user.password != encrypt(input.password):
            return output(430)

        session = web.ctx.session
        session['user_id'] = user.user_id
        session['login_name'] = user.login_name
        session['user_type'] = int(user.type)

        return output(200, {'type':int(user.type)})