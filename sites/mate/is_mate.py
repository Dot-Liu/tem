#!/usr/bin/python
#-*- coding: utf8 -*-

import web

from route import route
from database import *
from output import output

@route('/api/mate/check')

class MateCheck:
    def GET(self):
        return  output(200,MateCheck.CheckMate())

    @staticmethod
    def CheckMate():
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['type'] == '0':
            return output(410)
        is_mate = True
        db = getDb()
        results = db.select('userinfo',var = {'id':session['user_id']},
                            where = 'user_id = $id',
                            what = 'have_connect')
        if results[0].have_connect == '0':
            is_mate = False

        return {'is_mate':is_mate}