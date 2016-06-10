#!/usr/bin/python
# -*- coding: utf8 -*-

import web


from route import route
from output import *
from database import *

@route('/api/user/letter/detail/get')
class getLetterDetail:
    def POST(self):
        input = web.input(letter_id = None)
        if input.letter_id == None:
            return output(110)
        try:
            input.letter_id = int(input.letter_id)
        except:
            return output(111)

        db = getDb()
        result = db.select('letter_detail',var ={'id':input.letter_id},
                           where = 'letter_id = $id',
                           what = 'content,add_time')
        if len(result)==0:
            return output(450)

        try:
            db.update('letter',vars = {'id':input.letter_id}, where = "letter_id=$id",
                      have_read = '1')
        except:
            return output(700)

        return output(200,{'content':result[0].content,"add_time":result[0].add_time})

