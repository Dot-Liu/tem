#!/usr/bin/python
#-*- coding: utf8 -*-

from is_mate import *

@route('/api/mate/name/get')
class getMatename:
    def GET(self):
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == 0:
            return output(410)
        is_mate = MateCheck.CheckMate()
        if not is_mate['is_mate']:
            return output(450)
        db = getDb()
        results = db.select('mate',var = {'id':session['user_id'],'type':'1'},
                            where = 'user_id = $id and have_connect = $type',
                            what = 'mate_name')
        return output(200,{'mate_name':results[0].mate_name})
