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

ceo = ""
quote = ""

if not symbol:
    cursor.execute("SELECT symbol FROM stocks LIMIT 1")
    res = cursor.fetchone()
    if res:
        symbol = res["symbol"]

if symbol:
    cursor.execute("SELECT 1 FROM etfs WHERE symbol=%s", (symbol,))
    etf = bool(cursor.rowcount)

    if etf:
        cursor.execute("SELECT owner_name FROM owners INNER JOIN accounts ON owners.owner=accounts.owner INNER JOIN etfs ON accounts.id=etfs.controls_account_id WHERE etfs.symbol=%s", (symbol,))
        ceo = escape(cursor.fetchone()["owner_name"])
        cursor.execute("SELECT ceo_quote FROM ceos WHERE ceo=%s", (ceo,))
        res = cursor.fetchone()
        if res:
            quote = escape(res["ceo_quote"])
    else:
        cursor.execute("SELECT ceo_quote, ceos.ceo AS ceo FROM ceos INNER JOIN stocks ON ceos.ceo=stocks.ceo WHERE symbol=%s", (symbol,))
        res = cursor.fetchone()
        ceo = escape(res["ceo"])
        quote = escape(res["ceo_quote"])

    if not checked or etf:
        cursor.execute("""
            SELECT last_price FROM stocks WHERE symbol=%(symbol)s
            UNION
            SELECT (IFNULL(SUM(stocks.last_price), 0) + accounts.balance) / IFNULL((SELECT SUM(units) FROM owns AS o2 where o2.symbol=etfs.symbol), 1) AS last_price
            FROM etfs INNER JOIN accounts ON accounts.id=etfs.controls_account_id LEFT JOIN shares ON accounts.id=shares.owned_by_account_id LEFT JOIN stocks ON shares.symbol=stocks.symbol
            WHERE etfs.symbol=%(symbol)s""", {"symbol":symbol})
        last_price = format_ba(cursor.fetchone()["last_price"])
        cursor.execute("""SELECT COUNT(*) AS count FROM shares WHERE symbol=%(symbol)s UNION SELECT SUM(units) AS count FROM owns WHERE symbol=%(symbol)s""", {"symbol":symbol})
        shares = cursor.fetchone()["count"] or 0
        cursor.execute("SELECT COUNT(*) AS count FROM lent WHERE symbol=%s", (symbol,))
        lent = ((cursor.fetchone()["count"] or 0) / (shares or 1)) * 100
        cursor.execute("SELECT COUNT(*) AS count FROM lendables WHERE symbol=%s", (symbol,))
        lending_available = (cursor.fetchone()["count"] or 0)
        cursor.execute("SELECT COUNT(*) AS count FROM orders WHERE symbol=%s AND NOT EXISTS (SELECT 1 FROM option_order WHERE order_id=id)", (symbol,))
        open_orders = (cursor.fetchone()["count"] or 0)
    else:
        cursor.execute("""
            SELECT bid, ask, bid_table.symbol FROM
                (SELECT max(price) AS bid, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity>0 AND EXISTS (SELECT 1 FROM option_order WHERE option_order.order_id=orders.id AND option_order.strike_price=%(strike)s AND option_order.expiration=%(expr)s) GROUP BY symbol) AS bid_table
            LEFT JOIN
                (SELECT min(price) AS ask, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity<0 AND EXISTS (SELECT 1 FROM option_order WHERE option_order.order_id=orders.id AND option_order.strike_price=%(strike)s AND option_order.expiration=%(expr)s) GROUP BY symbol) AS ask_table
            ON bid_table.symbol=ask_table.symbol
            WHERE
                bid_table.symbol=%(symbol)s
            UNION
            SELECT bid, ask, ask_table.symbol AS symbol FROM
                (SELECT max(price) AS bid, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity>0 AND EXISTS (SELECT 1 FROM option_order WHERE option_order.order_id=orders.id AND option_order.strike_price=%(strike)s AND option_order.expiration=%(expr)s) GROUP BY symbol) AS bid_table
            RIGHT JOIN
                (SELECT min(price) AS ask, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity<0 AND EXISTS (SELECT 1 FROM option_order WHERE option_order.order_id=orders.id AND option_order.strike_price=%(strike)s AND option_order.expiration=%(expr)s) GROUP BY symbol) AS ask_table
            ON bid_table.symbol=ask_table.symbol
            WHERE ask_table.symbol=%(symbol)s
                    """, {"symbol":symbol, "strike":strike, "expr":expiry})
        res = cursor.fetchone()
        if res:
            last_price = format_ba(res['ask'] - res['bid'] if res['res'] and res['bid'] else None)
            cursor.execute("""SELECT COUNT(*) AS count FROM shares WHERE symbol=%(symbol)s UNION SELECT SUM(units) AS count FROM owns WHERE symbol=%(symbol)s""", {"symbol":symbol})
            shares = cursor.fetchone()["count"] or 0
            cursor.execute("SELECT COUNT(*) AS count FROM lent WHERE symbol=%s", (symbol,))
            lent = ((cursor.fetchone()["count"] or 0) / (shares or 1)) * 100
            cursor.execute("SELECT COUNT(*) AS count FROM lendables WHERE symbol=%s", (symbol,))
            lending_available = (cursor.fetchone()["count"] or 0)
            cursor.execute("SELECT COUNT(*) AS count FROM orders WHERE symbol=%s AND NOT EXISTS (SELECT 1 FROM option_order WHERE order_id=id)", (symbol,))
            open_orders = (cursor.fetchone()["count"] or 0)

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
                WHERE symbol=%(symbol)s AND EXISTS (SELECT 1 FROM option_order WHERE option_order.order_id=orders.id AND option_order.strike_price=%(strike)s AND option_order.expiration=%(expr)s)
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
                """, {"symbol":symbol, "strike":strike, "expr":expiry})
            found_sell = False
            for row in cursor:
                rows += 1
                orders += symbol_order.format(type="Limit" if row["is_limit"] else "Stop" if row["is_stop"] else "Market", buy_sell="Sell" if row["is_sell"] else "Buy", limit=format_ba(row["stop_price"] if row["stop_price"] else row["limit_price"]), count=-row["count"] if row["is_sell"] else row["count"])
                if not found_sell and row['is_sell']:
                    buy_end = rows
            orders = orders[12:]


buy_end += 3
buy_end_po = buy_end + 1
rows_0 = f"repeat({buy_end - 3}, 1fr)" if buy_end - 3 != 0 else ""
rows_1 = f"repeat({rows - buy_end + 3}, 1fr) " if rows - buy_end + 3 != 0 else ""

print(script_html.format(**globals()))