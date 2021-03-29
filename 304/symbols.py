#! /usr/bin/python3
from datetime import datetime
from ubcsx import script_html, names, symbols, current_page, params, escape, cursor, dollar, urlencode

symbol = escape(params["symbol"][0]) if "symbol" in params else ""
checked = "checked" if "option" in params else ""
today = escape(datetime.today().strftime('%Y-%m-%d'))
expiry = escape(params["expiry"][0]) if "expiry" in params else ""
strike = escape(params["strike"][0]) if "strike" in params else ""
symbol_url = escape(urlencode({"symbol":symbol}))

orders = ""
rows = 0

last_price = 0
shares = 0
lent = 0
lending_available = 0
open_orders = 0

if symbol:
    cursor.execute("SELECT 1 FROM etfs WHERE symbol=%s", (symbol,))

    if not checked or cursor.rowcount:
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
        cursor.execute("SELECT COUNT(*) AS count FROM orders WHERE symbol=%s", (symbol,))
        open_orders = (cursor.fetchone()["count"] or 0)



print(script_html.format(**globals()))