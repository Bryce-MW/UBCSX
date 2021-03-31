#! /usr/bin/python3
from ubcsx import cursor, post, redirect, script_html, urlencode, user, current_page, symbols, names

if not post:
    print(script_html.format(**globals()))
else:
    print(post)
    print(user)
    print(script_html.format(**globals()))

    if post["type"][0] == "Company":
        try:
            cursor.execute("SELECT symbol FROM stocks WHERE symbol = %s", (post["ipo-symbol"][0],))
            symbol = cursor.fetchone()
            cursor.execute("SELECT owner_name FROM owners WHERE owner = %s", (user,))
            owner_name = cursor.fetchone()["owner_name"]

            if symbol is not None:
                redirect("main.py", "A stock with that symbol already exists.")
                exit()

            cursor.execute("INSERT INTO ceos (ceo) VALUES %s", (owner_name,))
            cursor.execute("INSERT INTO stocks (name, symbol, ceo) VALUES (%(name)s, %(symbol)s, %(ceo)s)", {"name": post["ipo-name"], "symbol": post["ipo-symbol"], "ceo": owner_name})
        except (KeyError, IndexError):
            # Something was not specified for some reason. Consider adding warning
            print(script_html.format(**globals()))
            exit()
    else:
        try:
            cursor.execute("SELECT symbol FROM etfs WHERE symbol = %s", (post["ipo-symbol"][0],))
            symbol = cursor.fetchone()

            if symbol is not None:
                redirect("main.py", "An ETF with that symbol already exists.")
                exit()

            cursor.execute("INSERT INTO etfs (symbol, controls_account_id) VALUES (%(symbol)s, %(account_id)s)", {"symbol": post["ipo-symbol"], "account_id": user})
        except (KeyError, IndexError):
            # Something was not specified for some reason. Consider adding warning
            print(script_html.format(**globals()))
            exit()

    redirect(f"main.py", "IPO added successfully.")
