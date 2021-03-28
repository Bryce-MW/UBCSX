#! /usr/bin/python3
from ubcsx import cursor, post, redirect, script_html, urlencode, user, unescape, params, escape

cursor.execute("SELECT owner_name FROM owners WHERE owner=%s", (user,))
name = cursor.fetchone()["owner_name"]

if not post:
    print(script_html.format(**globals()))
else:
    if "account" in params:
        account_name = unescape(params["account"][0])
        try:
            new_name = post["name"][0]
        except (KeyError, IndexError):
            # Something was not specified for some reason. Consider adding warning
            print(script_html.format(**globals()))
            exit()
        cursor.execute("UPDATE owners SET owner_name=%s WHERE owner=%s", (new_name, user))
        encoded = urlencode({"account": account_name})
        redirect(f"main.py?{encoded}")
