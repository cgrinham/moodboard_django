#! /usr/bin/python
"import user's image into django database manually"

import sqlite3
from datetime import datetime
import sys


DATABASE = 'db.sqlite3'
cur_process = 'Image Importer'


def get_logtime():
    """ Return the date and time """
    return datetime.now().strftime('%Y/%m/%d %H:%M')

def insert_image(cur):
	cur.execute('INSERT INTO moodboard_UserImage(filename, directory, owner_id) VALUES(?, ?, ?)', (filename, directory, owner_id))
	con.commit()


con = None

try:
	con = sqlite3.connect(DATABASE)
	cur = con.cursor()
	print "%s - %s: Database connected" % (get_logtime(), cur_process)

	cur.execute('SELECT * FROM moodboard_UserImage;')
	#rows - cur..fetchall()
	rows = cur.fetchone()
	print rows[0]

except sqlite3.Error, e:
    print "%s - %s: Error %s: " % (get_logtime(), cur_process, e.args[0])
    sys.exit(1)

finally:
    if con:
        con.commit()
        #print "%s - %s: Changes Commited" % (get_logtime(), cur_process)
        con.close()
        #print "%s - %s: Database disconnected" % (get_logtime(), cur_process)
