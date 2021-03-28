#! /usr/bin/python3
from ubcsx import cursor, post, redirect, script_html, urlencode, user, current_page, symbols, names

if not post:
    print(script_html.format(**globals()))
else:
    try:
        cursor.execute("SELECT owner_name FROM owners WHERE owner = %s", (user,))
        owner_name = cursor.fetchone()["owner_name"]
        account_name = post["account_name"][0]
    except (KeyError, IndexError):
        # Something was not specified for some reason. Consider adding warning
        print(script_html.format(**globals()))
        exit()

    cursor.execute("SELECT account_name FROM accounts WHERE owner = %(user)s AND account_name = %(account_name)s", {"user": user, "account_name": account_name})
    acc = cursor.fetchone()

    if acc is not None:
        redirect("main.py", "An account with that name already exists.")
        exit()

    cursor.execute("INSERT INTO owners (owner, owner_name) VALUES (%(user)s, %(owner_name)s) ON DUPLICATE KEY UPDATE owner_name=%(owner_name)s", {"user": user, "owner_name": owner_name})
    cursor.execute("INSERT IGNORE INTO accounts (owner, account_name) VALUES (%(user)s, %(account_name)s)", {"user": user, "account_name": account_name})
    encoded = urlencode({"account": account_name})
    redirect(f"main.py?{encoded}", "Account added successfully.")
