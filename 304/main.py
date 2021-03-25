#! /usr/bin/python3
from ubcsx import script_html, user, redirect, post, cursor, escape, current_page
from templates import account_dropdown, option_value

cursor.execute("SELECT account_name FROM accounts WHERE owner=%s", (user,))
accounts = ""
for account in cursor:
    accounts += account_dropdown.format(account=escape(account["account_name"]))
accounts = accounts[16:]

cursor.execute("SELECT symbol FROM stocks UNION SELECT symbol FROM etfs")
symbols = ""
for symbol in cursor:
    symbols += option_value.format(value=escape(symbol["symbol"]))
symbols = symbols[8:]

cursor.execute("SELECT name FROM stocks UNION SELECT account_name AS name FROM accounts INNER JOIN etfs ON accounts.id=etfs.controls_account_id")
names = ""
for name in cursor:
    names += option_value.format(value=escape(name["name"]))
names = names[8:]

print(script_html.format(**globals()))