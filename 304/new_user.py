#! /usr/bin/python3
from ubcsx import cursor, post, redirect, script_html, urlencode, user

if not post:
    print(script_html.format(**globals()))
else:
    try:
        owner_name = post["name"][0]
        account_name = post["account_name"][0]
    except (KeyError, IndexError):
        # Something was not specified for some reason. Consider adding warning
        print(script_html.format(**globals()))
        exit()
    cursor.execute("INSERT INTO owners (owner, owner_name) VALUES (%(user)s, %(owner_name)s) ON DUPLICATE KEY UPDATE owner_name=%(owner_name)s", {'user': user, 'owner_name': owner_name})
    cursor.execute("INSERT IGNORE INTO accounts (owner, account_name) VALUES (%(user)s, %(account_name)s)", {'user': user, 'account_name': account_name})
    encoded = urlencode({"account": account_name})
    redirect(f"main.py?{encoded}")
