#! /bin/false
import atexit
import os.path
import urllib.parse
from urllib.parse import urlencode
import sys
from html import escape, unescape

import mysql.connector

from secret import dbpassword
class HTMLOut:
    def __init__(self, file_):
        self._file = file_

    def write(self, data):
        data = escape(data).replace("\n", "<br/>\n").expandtabs(2)
        result = '<span style="font-family: &quot;Fira Code&quot;, monospace">'
        for line in data.splitlines():
            without_indentation = line.lstrip()
            indentation_level = len(line) - len(without_indentation)
            result += f'<span style="margin-left: {indentation_level}ch">' + line.replace("<br/>", "</span><br/>\n")
        result += "</span>"
        return self._file.write(result)

    def __getattr__(self, attr):
         return getattr(self._file, attr)
sys.stderr = HTMLOut(sys.stdout)

print("Content-type: text/html\n")

dbuser = ""
script_filename = ""
user = ""
script_html = ""
post = None
params = None
try:
    user = os.environ["REMOTE_USER"]
    dbuser = os.environ["CONTEXT_PREFIX"][2:]
    script_filename = os.environ["SCRIPT_FILENAME"]
    if os.environ["REQUEST_METHOD"] == "POST":
        for line in sys.stdin:
            post = urllib.parse.parse_qs(line, keep_blank_values=True)
    if "QUERY_STRING" in os.environ:
        params = {k: unescape(v) for k,v in urllib.parse.parse_qs(os.environ["QUERY_STRING"], keep_blank_values=True).items()}
except KeyError:
    print("<HTML><body>The server must be broken. Check <code>ubcsx.py:12</code></body></HTML>")
    exit()

current_page = os.environ["SCRIPT_NAME"].split("/")[-1].split(".")[0]
dollar = 10000

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

script_html_name = ".".join(script_filename.split(".")[:-1]) + ".html"
if os.path.isfile(script_html_name):
    script_html = open(script_html_name, mode="r").read()


def redirect(url: str):
    if os.path.isfile("redirect.html"):
        print(open("redirect.html", mode="r").read().format(url=escape(url)))
    else:
        print(f"""<HTML><head><meta http-equiv="Refresh" content="1; url={escape(url)}"><link href="ubcsx.css" rel="stylesheet"></head><body class="gradient"></HTML>""")
