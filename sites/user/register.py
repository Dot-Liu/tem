#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import re
import random
import time

from route import route
from database import *
from sms import send_mail
from output import *
from encrypt import *

@route('/user/verify/send')
class SendMail:
    def POST(self):
        input = web.input(email = None)

        if input.email == None:
            return output(110)

        if not re.compile(r'(([a-z\-\.]|[0-9]))+@[a-z\-\.]+$').match(input.email):
            return output(120)


        db = getDb()
        results = db.select('user', vars = {'login_name' : input.email},
                            where = "login_name=$login_name", what = "user_id,type")

        is_register = True
        length = len(results)
        if length == 0:
            is_register = False
        else:
            user = results[0]
            if user.type == '2':
                is_register = False
        if not is_register:
            verify_code = str(random.randint(000000, 999999))
            status = send_mail(input.email,"欢迎注册 Oletter","\n您的验证码为"+verify_code+"\n该验证码在30分钟内有效")
            if status == -1:
                return output(701)

            t = db.transaction()
            try:
                if length == 0:
                    user_id = db.insert('user', login_name = input.email, type = '2')
                else:
                    user_id = user.user_id
                results = db.select('verify', vars = {'id':user_id}, where = "user_id=$id")
                if len(results) == 0:
                    db.insert('verify', user_id = user_id, verify_code = verify_code,
                              add_time = int(time.mktime(time.localtime())))
                else:
                    db.update('verify', vars = {'id':user_id},
                              where = "user_id=$id", verify_code = verify_code,
                              add_time = int(time.mktime(time.localtime())))
                t.commit()
            except:
                t.rollback()
                return output(700)

            return output(200, {'verify_code_md5' : encrypt(verify_code)})
        else:
            return output(420)


@route('/api/user/register')
class UserRegister:
    def POST(self):
        input = web.input(email = None,password = None,verify_code = None)
        if input.email == None or input.password == None or input.verify_code ==None:
            return output(110)

        if len(input.password) < 6 or len(input.password) > 18:
            return output(130)

        if not re.compile(r'[0-9A-Za-z_]+').match(input.password):
            return output(131)

        db = getDb()
        results = db.select('user', vars = {'name':input.email},
                            where = "login_name=$name", what = "type, user_id")

        if len(results) == 0:
            return output(431)

        user = results[0]
        if user.type != '2':
            return output(420)

        results = db.select('verify', vars = {'id':user.user_id, 'code':str(input.verify_code)},
                            where = "user_id=$id and verify_code=$code")
        if len(results) == 0:
            return output(431)

        t = db.transaction()
        try:
            db.update('user', vars = {'id':user.user_id}, where = "user_id=$id",
                      type = '1', password = encrypt(input.password))
            db.delete('verify', vars = {'id':user.user_id}, where = "user_id=$id")
            t.commit()
        except:
            t.rollback()
            return output(700)
        return output(200)

