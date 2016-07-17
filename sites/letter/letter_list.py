#!/usr/mport web

from database import *
from route import route
from output import *

@route('/api/letter/list')
class getLetterlist:
    def POST(self):
        input = web.input(is_refresh = 0, letter_count = 10, last_letter_id = None,have_read = None)
        try:
            input.is_refresh = int(input.is_refresh)
            input.letter_count = int(input.letter_count)
            if input.last_letter_id != None:
                input.last_letter_id = int(input.last_letter_id)
        except:
            return output(111)
	if input.last_letter_id ==None:
	    return output(110) 
        if input.have_read not in ('0','1'):
            return output(112)
        if input.letter_count <= 0:
            return output(112)

        session = web.ctx.session
        if not session.has_key('user_id'):
            return output(411)
        if session['user_type'] == '0':
            return output(410)
        db = getDb()
        res = db.select('userinfo',vars={'id':session['user_id'],'type':'1'},
                        where = 'user_id = $id and have_connect = $type')
        if len(res)==0:
            return output(450)
        rq = db.select('mate',vars = {'id':session['user_id']},
                       where = 'user_id =$id',
                       what = 'mate_id')
	ret = rq[0]
        if input.have_read!=None:
           # if input.is_refresh != 0 :
            results = db.select('letter',vars={'count':input.letter_count,'type':input.have_read,'user_id':session['user_id'],'sender_id':ret.mate_id},
                                where = "have_read=$type and user_id=$user_id and sender_id =$sender_id",
                                order = "add_time desc",
                                what = "letter_id,add_time,title")
            '''else:
                results = db.select('letter', vars={'sender_id':ret.mate_id,'count':input.letter_count,'type':input.have_read,'last_id':input.last_letter_id,'user_id':session['user_id']},
                                where = "have_read=$type and letter_id<$last_id and user_id=$user_id and sender_id = $sender_id",
                                order = "add_time desc",
                                what = "letter_id,add_time,title")'''
        else:
            #if input.is_refresh != 0 :
            results = db.select('letter', vars={'count':input.letter_count,'user_id':session['user_id'],'sender_id':ret.mate_id},
                                where = "user_id=$user_id and sender_id = $sender_id",
                                order = "add_time desc",
                                what = "letter_id,add_time,title")
            '''else:
                results = db.select('letter', vars={'count':input.letter_count,'last_id' : input.last_letter_id,'user_id':session['user_id'],'sender_id':ret.mate_id},
                                where = "letter_id<$last_id and user_id=$user_id and sender_id =$sender_id",
                                order = "add_time desc",
                                what = "letter_id,add_time,title")'''
        letter_list = []
        for i in results:
            letter_list.append({'letter_id' : i.letter_id, 'add_time' : i.add_time,'title':i.title})
        return output(200, letter_list)

