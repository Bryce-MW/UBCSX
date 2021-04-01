#! /usr/bin/python3
from html import escape
from ubcsx import cursor, post, redirect, script_html, urlencode, user, current_page, symbols, names

if not post:
    cursor.execute("SELECT account_name FROM accounts WHERE owner = %s", (user,))
    accounts = [row["account_name"] for row in cursor.fetchall()]
    accounts_html = "".join(f'<option value="{escape(i)}">{escape(i)}</option>"' for i in accounts)
    print(script_html.format(**globals()))
else:
    try:
        cursor.execute("SELECT owner_name FROM owners WHERE owner = %s", (user,))
        account_name = post["account_name"][0]
    except (KeyError, IndexError):
        # Something was not specified for some reason. Consider adding warning
        print(script_html.format(**globals()))
        exit()

    cursor.execute("DELETE FROM accounts WHERE owner = %(user)s AND account_name = %(account_name)s", {"user": user, "account_name": account_name})
    redirect("main.py?all", "Account removed successfully.")
