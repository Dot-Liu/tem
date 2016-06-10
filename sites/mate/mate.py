#!/usr/bin/python
#-*- coding: utf8 -*-

import web
import random
import time
from route import route
from output import *
from database import *
@route('/api/user/mate')

class Usermate:
    def POST(self):
        mate_time = int(time.mktime(time.localtime()))
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['type'] == '0':
            return output(410)

        db = getDb()
        result = db.select('userinfo',var = {'id':session['user_id']},
                           where  = 'user_id =$id',
                           what = 'have_connect')

        if result[0].have_connect == '1':
            return output(450)

        res = db.select('letter_detail',var ={'id':session['user_id']},
                        where = 'sender_id!=$id',
                        order = 'add_time desc',
                        what = 'sender_id')
        is_mate = False
        for i in res:
            mate = db.select('userinfo',var ={'id':i.sender_id},
                             where = 'user_id = $id',
                             what = 'user_id,have_connect')
            if mate[0].have_connect == '0':
                is_mate =True
                break
        if is_mate == False:
            return output(451)
        var = {'id1':session['user_id'],'id2':mate[0].user_id}
        t = db.transaction()
        try:
            db.update('mate',var,
                      where = 'user_id = $id1',mate_id = mate[0].user_id,
                      add_time = mate_time)
            db.update('mate',var,where = 'user_id=$id2',mate_id = session['user_id'],
                      add_time = mate_time)
            db.update('userinfo',var,
                      where = 'user_id =$id1 or user_id = $id2',have_connect = '1')
            rq =db.select('letter_detail',var = {'id1':mate[0].user_id,'id':'','id2':session['user_id']},
                          where = 'user_id = $id and (sender_id=$id1 or sender_id = $id2)',
                          what = 'letter_id,add_time')
            for i in rq:
                db.update('letter_detail',var ={'id': i.letter_id},
                        where = 'letter_id = $id',user_id =session['user_id'])
                db.insert('letter',user_id =session['user_id'],add_time =i.add_time,have_connect = '0',
                          letter_id = i.letter_id,sender_id = mate[0].user_id)
            t.commit()
        except:
            t.rollback()
            return output(700)
        return output(200)