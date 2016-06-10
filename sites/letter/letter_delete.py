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
        db = getDb()
        t = db.transaction()
        try:
            db.delete('letter',var = {'id':input.letter_id},
                      where = 'letter_id = $id')
            db.delete('letter_detail',var = {'id':input.letter_id},
                      where = 'letter_id = $id')
        except:
            t.rollback()
            return output(700)
        return output(200)