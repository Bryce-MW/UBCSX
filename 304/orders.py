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
        cursor.execute("""SELECT limit_table.price as limit_price, orders_prices.id as id, orders_prices.symbol as symbol, orders_prices.price as price FROM `limit` as limit_table INNER JOIN (SELECT orders.id as id, orders.symbol as symbol, stocks.last_price as price FROM orders INNER JOIN stocks ON orders.symbol=stocks.symbol) AS orders_prices ON orders_prices.id=limit_table.order_id""")
        for row in cursor:
            # print(row)
            rows += 1
            orders += order.format(symbol=escape(row['symbol']),
                                   symbol_url=escape(urlencode({"symbol": row['symbol']})),
                                   type="Limit",
                                   limit=float(row['limit_price']) / dollar,
                                   stop="",
                                   price=float(row['price']) / dollar,
                                   id=row['id'])
        #
        cursor.execute("""SELECT stop.price as stop, stop.limit_price as limit_price, orders_prices.id as id, orders_prices.symbol as symbol, orders_prices.price as price FROM stop INNER JOIN (SELECT orders.id as id, orders.symbol as symbol, stocks.last_price as price FROM orders INNER JOIN stocks ON orders.symbol=stocks.symbol) AS orders_prices ON orders_prices.id=stop.order_id""")
        for row in cursor:
            # print(row)
            rows += 1
            orders += order.format(symbol=escape(row['symbol']),
                                   symbol_url=escape(urlencode({"symbol": row['symbol']})),
                                   type="Stop",
                                   limit=float(row['limit_price']) / dollar,
                                   stop=float(row['stop']) / dollar,
                                   price=float(row['price']) / dollar,
                                   id=row['id'])

        cursor.execute("""SELECT orders.id as id, orders.symbol as symbol, stocks.last_price as price FROM orders INNER JOIN stocks ON orders.symbol=stocks.symbol WHERE orders.id NOT IN (SELECT order_id FROM `limit`) AND orders.id NOT IN (SELECT order_id FROM stop)""")
        for row in cursor:
            # print(row)
            rows += 1
            orders += order.format(symbol=escape(row['symbol']),
                                   symbol_url=escape(urlencode({"symbol": row['symbol']})),
                                   type="Market",
                                   limit="",
                                   stop="",
                                   price=float(row['price']) / dollar,
                                   id=row['id'])
        orders = orders[12:]
        print(script_html.format(**globals()))
    else:
        # print(post)
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
            # print(order_id)
            if 'option' in post:
                # print("Option")
                cursor.execute("INSERT INTO option_order (strike_price, expiration, order_id) VALUES (%s, %s, %s)",
                               (strike_price, expiry, order_id))

            if post['type'][0] == "Limit":
                # print("Limit")
                cursor.execute("INSERT INTO `limit` (price, order_id) VALUES (%s, %s)",
                               (limit, order_id))
            elif post['type'][0] == "Stop":
                # print("Stop")
                cursor.execute("INSERT INTO stop (price, limit_price, order_id) VALUES (%s, %s, %s)",
                               (stop, limit, order_id))
            redirect(f"orders.py?account={account_name}", "Order successfully added!")

else:
    print("Error: account name not provided")
