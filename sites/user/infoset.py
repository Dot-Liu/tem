#!/usr/bin/python
#-*- coding: utf8 -*-

import web
import re

from route import route
from database import *
from output import output

@route('/api/user/infoset')
class infoSet:
    def POST(self):
	input = web.input(name=None,is_male=None)
        return infoSet.SetInfo(name= input.name,is_male=input.is_male)
    @staticmethod
    def SetInfo(name=None,is_male=None,user_id=None):
        if name==None or is_male==None:
            return output(110)
        try:
            is_male  =int(is_male)
            if is_male not in (0,1):
                return output(112)
        except:
            return output(111)
        if len(name)<=0 or len(name)>20:
            return output(113)
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == 0:
            return output(410)

        if is_male==1:
            sex = "male"
        else:
            sex = "female"

        db=getDb()
	if user_id ==None:
            user_id=session['user_id']
        results = db.select('userinfo',vars = {'id':user_id},
                            where = 'user_id =$id')
        if len(results)==1:
            try:
                db.update('userinfo',vars = {'id':user_id},where = 'user_id=$id',
                          name = name,gender=sex)
            except:
                return output(700)
        else:
            try:
                info_id= db.insert("userinfo",user_id = user_id, name=name,gender=sex,have_connect = '0')
	    except:
                return output(700)
        return output(200)
