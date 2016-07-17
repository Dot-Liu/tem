#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import time
from database import *
from route import route
from output import *
import sys
sys.path.append("/root/Oletter/sites/mate")
import mate,is_mate
import json
from mate import *
from is_mate import *
@route('/api/letter/send')

class letterSend:
    def POST(self):
        input = web.input(content = None)
        if input.content ==None:
            return output(110)
        send_time = int(time.mktime(time.localtime()))
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == 0:
            return output(410)
	mateCheck = json.loads(MateCheck.CheckMate())
	print mateCheck
	if mateCheck['data']['is_mate'] == False:
	    Usermate.MateUser()
        db = getDb()
        results = db.select('userinfo',vars = {'id':session['user_id']},
                            where = 'user_id=$id')
        res = results[0]
        if res.have_connect == '0':
            t = db.transaction()
            try:
                db.insert('letter_detail',sender_id = session['user_id'],sender_name = res.name,add_time = send_time,title = input.content[0:20],content =input.content)
                t.commit()
            except:
                t.rollback()
                return output(700)
        else:
            rq = db.select('mate',vars ={'id':session['user_id']},
                           where = 'user_id=$id',
                           what = 'mate_id')
	    user = rq[0]
            t = db.transaction()
            try:
                db.insert('letter_detail',sender_id = session['user_id'],sender_name = res.name,add_time = send_time,
                              title = input.content[0:20],content =input.content,user_id = user.mate_id)
                id = db.select('letter_detail',vars = {'title':input.content[0:20]},
                               where = 'title =$title',
                               what = 'letter_id')
                db.insert('letter',title = input.content[0:20],user_id = user.mate_id,sender_id = session['user_id'],letter_id = id[0].letter_id,add_time = send_time,have_read = '0')

                t.commit()
            except:
                t.rollback()
                return output(700)
        return output(200)
