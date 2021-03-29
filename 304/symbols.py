#! /usr/bin/python3
from datetime import datetime
from ubcsx import script_html, names, symbols, current_page, params, escape, cursor, dollar, urlencode, format_ba
from templates import symbol_order

symbol = escape(params["symbol"][0]) if "symbol" in params else ""
checked = "checked" if "option" in params else ""
today = escape(datetime.today().strftime('%Y-%m-%d'))
expiry = escape(params["expiry"][0]) if "expiry" in params else ""
strike = escape(params["strike"][0]) if "strike" in params else ""
symbol_url = escape(urlencode({"symbol":symbol}))

orders = ""
rows = 0
buy_end = 0

last_price = 0
shares = 0
lent = 0
lending_available = 0
open_orders = 0

if symbol:
    cursor.execute("SELECT 1 FROM etfs WHERE symbol=%s", (symbol,))
    etf = bool(cursor.rowcount)

    if not checked or etf:
        cursor.execute("""
            SELECT last_price FROM stocks WHERE symbol=%(symbol)s
            UNION
            SELECT (IFNULL(SUM(stocks.last_price), 0) + accounts.balance) / IFNULL((SELECT SUM(units) FROM owns AS o2 where o2.symbol=etfs.symbol), 1) AS last_price
            FROM etfs INNER JOIN accounts ON accounts.id=etfs.controls_account_id LEFT JOIN shares ON accounts.id=shares.owned_by_account_id LEFT JOIN stocks ON shares.symbol=stocks.symbol
            WHERE etfs.symbol=%(symbol)s""", {"symbol":symbol})
        last_price = (cursor.fetchone()["last_price"] or 0) / dollar
        cursor.execute("""SELECT COUNT(*) AS count FROM shares WHERE symbol=%(symbol)s UNION SELECT SUM(units) AS count FROM owns WHERE symbol=%(symbol)s""", {"symbol":symbol})
        shares = cursor.fetchone()["count"] or 0
        cursor.execute("SELECT COUNT(*) AS count FROM lent WHERE symbol=%s", (symbol,))
        lent = ((cursor.fetchone()["count"] or 0) / (shares or 1)) * 100
        cursor.execute("SELECT COUNT(*) AS count FROM lendables WHERE symbol=%s", (symbol,))
        lending_available = (cursor.fetchone()["count"] or 0)
        cursor.execute("SELECT COUNT(*) AS count FROM orders WHERE symbol=%s AND NOT EXISTS (SELECT 1 FROM option_order WHERE order_id=id)", (symbol,))
        open_orders = (cursor.fetchone()["count"] or 0)
    else:
        pass
        # This is an option...

    if not etf:
        if not checked:
            cursor.execute("""
                SELECT
                    EXISTS (SELECT 1 FROM `limit` AS l2 WHERE l2.order_id=orders.id) AS is_limit,
                    EXISTS (SELECT 1 FROM stop AS s2 WHERE s2.order_id=orders.id) AS is_stop,
                    orders.quantity < 0 AS is_sell,
                    `limit`.price AS limit_price,
                    stop.price AS stop_price,
                    SUM(orders.quantity) AS count
                FROM orders
                    LEFT JOIN `limit` ON orders.id=`limit`.order_id
                    LEFT JOIN stop ON orders.id=stop.order_id
                WHERE symbol=%s
                GROUP BY
                    is_sell,
                    is_limit,
                    is_stop,
                    `limit`.price,
                    stop.price
                ORDER BY
                    is_sell ASC,
                    IFNULL(stop.price, `limit`.price) ASC,
                    is_limit ASC,
                    is_stop ASC
                """, (symbol,))
            found_sell = False
            for row in cursor:
                rows += 1
                orders += symbol_order.format(type="Limit" if row["is_limit"] else "Stop" if row["is_stop"] else "Market", buy_sell="Sell" if row["is_sell"] else "Buy", limit=format_ba(row["stop_price"] if row["stop_price"] else row["limit_price"]), count=-row["count"] if row["is_sell"] else row["count"])
                if not found_sell and row['is_sell']:
                    buy_end = rows
            orders = orders[12:]
        else:
            pass
            # This is an option...


buy_end += 3
buy_end_po = buy_end + 1
rows_0 = f"repeat({buy_end - 3}, 1fr)" if buy_end - 3 != 0 else ""
rows_1 = f"repeat({rows - buy_end + 3}, 1fr) " if rows - buy_end + 3 != 0 else ""

print(script_html.format(**globals()))