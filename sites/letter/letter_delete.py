#!/usr/bin/python
# -*- coding: utf8 -*-

import web

from database import *
from route import route
from output import *

@route('/api/letter/delete')
class DeleteLetter:
    def POST(self):
        input = web.input(letter_id = None)
        if input.letter_id ==None:
            return output(110)
        try:
            input.letter_id = int(input.letter_id)
        except:
            return output(111)
	session = web.ctx.session
	if not session.has_key('user_id'):
	    return output(411)
	if session['user_type']=='0':
	    return output(410)
        db = getDb()
	results = db.select('letter_detail',vars ={'id':input.letter_id},
			    where = 'letter_id= $id')
	if len(results)==0:
	    return output(470)
        t = db.transaction()
        try:
            db.delete('letter',vars = {'id':input.letter_id},
                      where = 'letter_id = $id')
            db.delete('letter_detail',vars = {'id':input.letter_id},
                      where = 'letter_id = $id')
	    t.commit()
        except:
            t.rollback()
            return output(700)
        return output(200)
