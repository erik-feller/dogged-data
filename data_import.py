###############################################################################
# 
# Script to move data from the old sqlite method of storing to postgresql
# Erik Feller
# 4/11/2019
#
###############################################################################

import psycopg2
import sqlite3

from lib.dog_class import Dog 

conn = sqlite3.connect('main.sqlite')
cur = conn.cursor()

#load all the rows from dogdata that are complete
cur.execute('SELECT * FROM dogdata WHERE out_time IS NOT NULL')

#iterate over each entry
rows = cur.fetchall()
for current_row in rows:
    print(current_row)
    #even though its not really effecient I'm going to 
    #create a dog and test the dog to Postgres function
    cur_dog = Dog(None, current_row[0], current_row[1], current_row[2], current_row[3], current_row[5], current_row[4], current_row[7], current_row[9])
    try:
        db_conn = psycopg2.connect("dbname='dogdata' user='dogdata' host='localhost' password='password'");
        cursor = db_conn.cursor()
        cursor.execute(cur_dog.sql_insert_print())
        db_conn.commit()
    except Exception as e:
        print(e)


