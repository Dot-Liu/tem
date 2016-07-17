#!/usr/bin/python
#-*- coding: utf8 -*-

import web

from route import route
from database import *
from output import output
from is_mate import *
import json
@route('/api/mate/name/get')
class getMatename:
    def GET(self):
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == 0:
            return output(410)
        is_mate = json.loads(MateCheck.CheckMate())
        if not is_mate['data']['is_mate']:
            return output(450)
        db = getDb()

	results = db.select('mate',vars = {'id':session['user_id']},
                            where = 'user_id = $id',
                            what = 'mate_id')
        res = db.select('userinfo',vars = {'id':results[0].mate_id},
                        where = 'user_id = $id',
                        what = 'name'
                        )
        return output(200,{'mate_name':res[0].name})
