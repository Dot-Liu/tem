#!/usr/bin/python
#-*- coding: utf8 -*-

import web
import random
import time
from route import route
from output import *
from database import *
@route('/api/mate')

class Usermate:
    def POST(self):
	return Usermate.MateUser()
    @staticmethod
    def MateUser():
	mate_time = int(time.mktime(time.localtime()))
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == '0':
            return output(410)

        db = getDb()
        result = db.select('userinfo',vars = {'id':session['user_id']},
                           where  = 'user_id =$id',
                           what = 'have_connect')

        if result[0].have_connect == '1':
            return output(450)

        res = db.select('letter_detail',vars ={'id':session['user_id']},
                        where = 'sender_id!=$id',
                        order = 'add_time desc',
                        what = 'sender_id')
        is_mate = False
        for i in res:
            mate = db.select('userinfo',vars ={'id':i.sender_id},
                             where = 'user_id = $id',
                             what = 'user_id,have_connect')
            matcher = mate[0]
            if matcher.have_connect == '0':
                is_mate =True
                break
        if is_mate == False:
            return output(451)

        t = db.transaction()
        try:
            if len(db.select('mate',vars={'id':session['user_id']},where='user_id=$id'))!=0:
                db.update('mate',vars={'id':session['user_id']},
			  where = 'user_id = $id',mate_id = matcher.user_id,
                          add_time = mate_time)
            else:
                db.insert('mate',user_id = session['user_id'],mate_id = matcher.user_id,add_time =mate_time)
            if len(db.select('mate',vars={'id':matcher.user_id},where='user_id=$id'))!=0:
                db.update('mate',vars={'id':matcher.user_id},
                          where = 'user_id=$id',mate_id = session['user_id'], add_time = mate_time)
            else:
                db.insert('mate',user_id =matcher.user_id,mate_id = session['user_id'], add_time = mate_time)
            db.update('userinfo',vars={'id1':session['user_id'],'id2':matcher.user_id},
                      where = 'user_id =$id1 or user_id = $id2',have_connect = '1')
            rq =db.select('letter_detail',vars = {'id1':matcher.user_id,'id':0,'id2':session['user_id']},
                          where = 'user_id = $id and (sender_id=$id1 or sender_id = $id2)',
                          what = 'letter_id,add_time,sender_id,title')
            for i in rq:
                print i.sender_id
                if i.sender_id!=session['user_id']:
                    db.update('letter_detail',vars ={'id': i.letter_id},
                              where = 'letter_id = $id',user_id =session['user_id'])
                    db.insert('letter',title =i.title,user_id =session['user_id'],add_time =i.add_time,have_read = '0',
                              letter_id = i.letter_id,sender_id = matcher.user_id)
                else:
                    db.update('letter_detail',vars ={'id': i.letter_id},
                              where = 'letter_id = $id',user_id =matcher.user_id)
                    db.insert('letter',title = i.title,user_id =matcher.user_id,add_time =i.add_time,have_read = '0',
                              letter_id = i.letter_id,sender_id = session['user_id'])
            t.commit()
        except:
            t.rollback()
            return output(700)
        return output(200)
