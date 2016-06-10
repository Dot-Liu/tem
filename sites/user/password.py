#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import re
import random
import time

from route import route
from encrypt import *
from output import *
from sms import send_mail
from database import *

@route('/api/user/password/forget')
class UserPasswordForget:
    def POST(self):
        input = web.input(email = None)

        if input.email == None:
            return output(110)

        db = getDb()
        results = db.select('user', vars = {'login_name' : input.email},
                            where = "login_name=$email and type!='2'", what = "user_id")
        if len(results) == 0:
            return output(422)

        user_id = results[0].user_id

        verify_code = str(random.randint(000000, 999999))
        status = send_mail(input.email,"密码找回确认","\n您的验证码为"+verify_code+"\n该验证码在30分钟内有效")
        if status == -1:
            return output(421)

        t = db.transaction()
        try:
            results = db.select('verify', vars = {'id':user_id}, where = "user_id=$id")
            if len(results) == 0:
                db.insert('verify', user_id = user_id, verify_code = str(verify_code),
                          add_time = int(time.mktime(time.localtime())))
            else:
                db.update('verify', vars = {'id':user_id}, where = "user_id=$id",
                          verify_code = str(verify_code), add_time = int(time.mktime(time.localtime())))
            t.commit()
        except:
            t.rollback()
            return output(700)

        return output(200, {'verify_code_md5' : encrypt(verify_code)})

@route('/api/user/password/verify')
class UserPasswordVerify:
    def POST(self):
        input = web.input(email = None, verify_code = None, new_password = None)
        if input.email == None or input.verify_code == None or input.new_password == None:
            return output(110)
        try:
            input.verify_code=int(input.verify_code)
        except:
            return output(111)
        if len(input.new_password) < 6 or len(input.new_password) > 18:
            return output(130)

        if not re.compile(r'[0-9A-Za-z_]+').match(input.new_password):
            return output(131)

        db = getDb()
        results = db.select('user', vars = {'name':input.email}, where = "login_name=$name and type!='2'",
                            what = "user_id")
        if len(results) == 0:
            return output(422)

        user_id = results[0].user_id
        if len(db.select('verify', vars = {'id':user_id, 'code':str(input.verify_code)},
                         where = "user_id=$id and verify_code=$code")) == 0:
            return output(431)
        else:
            t = db.transaction()
            try:
                vars = {'id':user_id}
                where = "user_id=$id"
                db.update('user',vars = vars, where = where, password = encrypt(input.new_password))
                db.delete('verify', vars = vars, where = where)
                t.commit()
            except:
                t.rollback()
                return output(700)
        return output(200)

@route('/api/user/password/change')
class UserPasswordChange:
    def POST(self):
        input = web.input(old_password = None, new_password = None)
        if input.old_password == None or input.new_password == None:
            return output(110)

        if len(input.new_password) < 6 or len(input.new_password) > 18:
            return output(130)

        if not re.compile(r'[0-9A-Za-z_]+').match(input.new_password):
            return output(131)

        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)

        db = getDb()
        password = db.select('user', vars = {'id':session['user_id']}, where = "user_id=$id",
                             what = "password")[0].password
        if password == encrypt(input.old_password):
            try:
                db.update('user', vars = {'id':session['user_id']}, where = 'user_id=$id',
                          password = encrypt(input.new_password))
                return output(200)
            except:
                return output(700)
        else:
            return output(430)


