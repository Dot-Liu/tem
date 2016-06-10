#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import re
from route import route
from database import *
from sms import send_mail
from output import *
from encrypt import *

@route('/user/info/set')
class UserInfoSet:
    def POST(self):
        input =web.input(name=None,email = None,address = None,qq=None,phone =None,is_male=None)
        if input.name==None or input.addresss==None or input.is_male==None:
            return output(110)
        try:
            input.is_male  =int(input.is_male)
            if input.is_male not in (0,1):
                return output(112)
        except:
            return output(111)

        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == 0:
            return output(410)
        if input.qq!=None:
            if not re.compile(r'^[1-9][0-9]+$').match(input.qq) or len(input.qq)>11:
                return output(112)
        '''if input.birthday!=None:
            if not re.compile(r'^[0-9]{4}-(0[1-9])|(1[0-2])-((0[1-9])|([1-2][0-9])|(3[0-1]))$').match(input.birthday):
                return output(112)
            date =re.split('-',input.birthday)
            try:
                year =int(date[0])
                month=int(date[1])
                day =int(date[2])
                if day ==0:
                    return output(112)
            except:
                return output(111)
            if month in (1,3,5,7,8,10,12):
                if day>31:
                    return output(112)
            if month in(4,6,9,11):
                if day>30:
                    return output(112)
            if month==2:
                if year%400==0 or (year%4==0 and year%100!=0):
                    if day>29:
                        return output(112)
                else:
                    if day>28:
                        return output(112)
                        '''
        if input.is_male==1:
            sex = "male"
        else:
            sex = "female"
        db=getDb()
        user_id=session['user_id']

        try:
            db.update("userinfo",vars ={"user_id":user_id},
                      where = "user_id=$user_id",
                      name=input.name,email = input.email, address=input.address,
                      qq=input.qq,phone=input.phone,gender=sex)
        except:
            return output(700)
        return output(200)

@route('/api/user/info/check')
class UserInfoCheck:
    def POST(self):
        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == 0:
            return output(410)
        user_id = session['user_id']
        db =getDb()
        result = db.select('userinfo',var ={'user_id':user_id},
                           where = 'user_id=$user_id',
                           what = 'name,email,address,qq,phone,gender')
        res = result[0]
        return output(200,{'name':res.name,'email':res.email,'address':res.address,
                           'qq':res.qq,'phone':res.phone,'gender':res.gender})