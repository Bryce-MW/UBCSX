#! /usr/bin/python3
from ubcsx import cursor, post, redirect, script_html, urlencode, user, current_page, symbols, names

if not post:
    print(script_html.format(**globals()))
else:
    print(script_html.format(**globals()))

    if post["type"][0] == "Company":
        try:
            cursor.execute("SELECT symbol FROM stocks WHERE symbol = %s", (post["ipo-symbol"][0],))
            symbol = cursor.fetchone()
            cursor.execute("SELECT owner_name FROM owners WHERE owner = %s", (user,))
            owner_name = cursor.fetchone()["owner_name"]
            cursor.execute("SELECT id FROM accounts WHERE owner = %s", (user,))
            account_id = cursor.fetchone()["id"]
            cursor.execute("SELECT ceo FROM ceos WHERE ceo = %s", (owner_name,))
            ceo = cursor.fetchone()

            if symbol is not None:
                redirect("main.py?all", "A stock with that symbol already exists.")
                exit()

            if ceo is None:
                cursor.execute("INSERT INTO ceos (ceo) VALUES (%s)", (owner_name,))

            cursor.execute("INSERT INTO stocks (name, symbol, ceo) VALUES (%(name)s, %(symbol)s, %(ceo)s)", {"name": post["ipo-name"][0], "symbol": post["ipo-symbol"][0], "ceo": owner_name})

            for i in range(int(post["ipo-shares"][0])):
                cursor.execute("INSERT INTO shares (symbol, owned_by_account_id) VALUES (%(symbol)s, %(account_id)s)", {"symbol": post["ipo-symbol"][0], "account_id": account_id})
        except (KeyError, IndexError):
            # Something was not specified for some reason. Consider adding warning
            print(script_html.format(**globals()))
            exit()
    else:
        try:
            cursor.execute("SELECT symbol FROM etfs WHERE symbol = %s", (post["ipo-symbol"][0],))
            symbol = cursor.fetchone()
            cursor.execute("SELECT id FROM accounts WHERE owner = %s", (user,))
            account_id = cursor.fetchone()["id"]
            cursor.execute("SELECT * FROM etfs WHERE controls_account_id = %s", (account_id,))
            etf = cursor.fetchone()

            if symbol is not None:
                redirect("main.py?all", "An ETF with that symbol already exists.")
                exit()
            elif etf is not None:
                redirect("main.py?all", "You already have an ETF.")
                exit()

            cursor.execute("INSERT INTO etfs (symbol, controls_account_id) VALUES (%(symbol)s, %(account_id)s)", {"symbol": post["ipo-symbol"][0], "account_id": account_id})
        except (KeyError, IndexError):
            # Something was not specified for some reason. Consider adding warning
            print(script_html.format(**globals()))
            exit()

    redirect("main.py?all", "IPO added successfully.")
