#! /usr/bin/python3
from templates import order
from ubcsx import script_html, cursor, names, symbols, current_page, params, unescape, post, user, escape, urlencode, \
    dollar, redirect

orders = ""
rows = 0

if "account" in params:
    account_name = unescape(params["account"][0])
    cursor.execute("SELECT id FROM accounts WHERE owner=%s AND account_name=%s", (user, account_name))
    account_id = cursor.fetchone()["id"]
    if not post:
        # cursor.execute()
        # for row in cursor:
        #     print(row)
        # rows += 1
        # orders += order.format(symbol=escape(row['symbol']),
        #                        symbol_url=escape(urlencode({"symbol": row['symbol']})),
        #                        type=row['type'],
        #                        limit=float(row['limit']) / dollar if (row['type'] == 'Limit') else "",
        #                        stop=float(row['stop']) / dollar if (row['type'] == 'Stop') else "",
        #                        price=float(row['value']) / dollar,
        #                        id=row['id'],
        #                            option=row['option'])
        rows += 1
        orders += order.format(symbol="AAPL",
                               symbol_url=escape(urlencode({"symbol": "AAPL"})),
                               type="Limit",
                               limit=float("3245345") / dollar if ("Limit" == 'Limit') else "",
                               stop=float("3245345") / dollar if ("Limit" == 'Stop') else "",
                               price=float("3245345") / dollar,
                               id=10,
                               option="on")
        orders = orders[12:]
        print(script_html.format(**globals()))
    else:
        print(post)
        if 'delete' in post:
            cursor.execute("DELETE FROM orders WHERE id = %s", (post['delete'][0],))
            redirect(f"orders.py?account={account_name}", "Order successfully deleted!")
        else:
            expiry = post['expiry'][0]
            count = int(post['count'][0]) if post['action'] == "Buy" else -int(post['count'][0])
            symbol = post['symbol'][0]
            limit = float(post['limit'][0]) * dollar
            stop = float(post['stop'][0]) * dollar
            strike_price = float(post['strike_price'][0]) * dollar

            cursor.execute(
                "INSERT INTO orders (valid_until, quantity, symbol, made_by_account_id) VALUES (%s, %s, %s, %s)",
                (expiry, count, symbol, account_id))

            cursor.execute("SELECT LAST_INSERT_ID()")
            order_id = cursor.fetchone()['LAST_INSERT_ID()']
            print(order_id)
            if 'option' in post:
                print("Option")
                cursor.execute("INSERT INTO option_order (strike_price, expiration, order_id) VALUES (%s, %s, %s)",
                               (strike_price, expiry, order_id))

            if post['type'][0] == "Limit":
                print("Limit")
                cursor.execute("INSERT INTO `limit` (price, order_id) VALUES (%s, %s)",
                               (limit, order_id))
            elif post['type'][0] == "Stop":
                print("Stop")
                cursor.execute("INSERT INTO stop (price, limit_price, order_id) VALUES (%s, %s, %s)",
                               (stop, limit, order_id))
            redirect(f"orders.py?account={account_name}", "Order successfully added!")

else:
    print("Error: account name not provided")
