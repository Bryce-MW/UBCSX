#! /bin/false
import atexit
import os
from html import escape

import mysql.connector

from secret import dbpassword

print("Content-type: text/html\n")

dbuser = ""
try:
    user = os.environ["REMOTE_USER"]
    dbuser = os.environ["CONTEXT_PREFIX"][2:]
except KeyError:
    print("<HTML><body>The server must be broken. Check <code>ubcsx.py:12</code></body></HTML>")
    exit()

database = None
cursor = None

try:
    database = mysql.connector.connect(user=dbuser, password=dbpassword, host='dbserver.students.cs.ubc.ca', database=dbuser, autocommit=True)
    cursor = database.cursor(dictionary=True, buffered=True)
except mysql.connector.Error as err:
    print("Something went wrong with the database connection:")
    print(err)
    exit(1)


def exit_handler():
    database.commit()
    database.disconnect()


atexit.register(exit_handler)


def redirect(url: str):
    print(f"""<HTML>

<meta http-equiv="Refresh" content="1; url={escape(url)}">

</HTML>""")
