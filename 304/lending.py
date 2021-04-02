#! /usr/bin/python3
from templates import lending
from ubcsx import script_html, cursor, names, symbols, current_page, params, unescape, post, user, escape, urlencode, \
    dollar, redirect

default_symbol = ""
lendings = ""
rows = 0

if "account" in params:
    account_name = unescape(params["account"][0])
    cursor.execute("SELECT id FROM accounts WHERE owner=%s AND account_name=%s", (user, account_name))
    if 'symbol' in params:
        default_symbol = params["symbol"][0]
    account_id = cursor.fetchone()["id"]
    if not post:
        offers = []
        cursor.execute("SELECT DISTINCT symbol, premium FROM lendables WHERE account_id=%s", (account_id,))
        for row in cursor:
            offers.append(row)
            print(row)
        for row in offers:
            symbol = row['symbol']
            premium = row['premium']
            cursor.execute(
                "SELECT COUNT(*) AS count FROM lendables WHERE symbol=%s AND premium=%s",
                (symbol, premium))
            count = cursor.fetchone()['count']
            rows += 1
            lendings += lending.format(symbol=escape(symbol),
                                       symbol_url=escape(urlencode({"symbol": symbol})),
                                       premium=float(premium) * 100,
                                       count=int(count))
        lendings = lendings[12:]
        print(script_html.format(**globals()))
    else:
        print(post)
        count = int(post['count'][0])
        symbol = post['symbol'][0]
        max_premium = float(post['premium'][0]) / 100

        if post['action'][0] == "Offer":
            cursor.execute("SELECT id as share_id FROM shares WHERE owned_by_account_id=%s AND symbol=%s", (account_id, symbol))
            share_id = cursor.fetchone()["share_id"]

            for i in range(count):
                cursor.execute(
                    "INSERT INTO lendables (premium, symbol, share_id, account_id) VALUES (%s, %s, %s, %s)",
                    (max_premium, symbol, share_id, account_id))

            redirect(f"lending.py?account={account_name}", f"{count} shares were offered.")

        else:
            bought_count = 0
            cursor.execute("SELECT premium, share_id, account_id as offering_account_id FROM lendables WHERE symbol=%s AND premium<%s AND account_id<>%s ORDER BY premium", (symbol, max_premium, account_id))
            for row in cursor:
                if bought_count > count:
                    break
                bought_count += 1

                premium = row['premium'][0]
                share_id = row['share_id'][0]
                offering_account_id = row['offering_account_id'][0]

                cursor.execute(
                    "INSERT INTO lent (premium, symbol, share_id, by_account_id, to_account_id) VALUES (%s, %s, %s, %s, %s)",
                    (premium, symbol, share_id, offering_account_id, account_id))

                cursor.execute(
                    "DELETE FROM lendables WHERE id IN (SELECT id FROM lendables WHERE premium=%s AND symbol=%s AND account_id=%s AND share_id=%s LIMIT 1)",
                    (premium, symbol, offering_account_id, share_id))

            redirect(f"lending.py?account={account_name}", f"{bought_count} shares were lent.")

else:
    print("Error: account name not provided")
