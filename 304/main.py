#! /usr/bin/python3
from templates import account_dropdown, option_value, position
from ubcsx import cursor, dollar, escape, params, script_html, unescape, urlencode, user

cursor.execute("SELECT account_name FROM accounts WHERE owner=%s", (user,))
accounts = ""
for account in cursor:
    accounts += account_dropdown.format(account=escape(account["account_name"]), account_escaped=urlencode({"account": account["account_name"]}), selected=account["account_name"] == params["account"][0])
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

if "account" in params:
    account_name = unescape(params["account"][0])
    cursor.execute("SELECT balance FROM accounts WHERE owner=%s AND account_name=%s", (user, account_name))
    cash = cursor.fetchone()["balance"]
    cursor.execute("SELECT SUM(stocks.last_price) AS value FROM shares INNER JOIN stocks ON shares.symbol=stocks.symbol INNER JOIN accounts ON accounts.id=shares.owned_by_account_id WHERE owner=%(user)s AND account_name=%(account)s", {"user": user, "account": account_name})
    market_value = cursor.fetchone()['value'] or 0
    cursor.execute("SELECT SUM((stocks.last_price + accounts.balance) / (owns.units / (SELECT SUM(units) FROM owns AS o2 where o2.symbol=owns.symbol))) AS value FROM shares INNER JOIN stocks ON shares.symbol=stocks.symbol INNER JOIN accounts ON accounts.id=shares.owned_by_account_id INNER JOIN etfs ON accounts.id=etfs.controls_account_id INNER JOIN owns ON owns.symbol=etfs.symbol INNER JOIN accounts AS a2 ON a2.id=owns.account_id WHERE a2.owner=%(user)s AND a2.account_name=%(account)s",
                   {"user": user, "account": account_name})
    market_value += cursor.fetchone()['value'] or 0
    total_equity = cash + market_value
    cursor.execute("SELECT COUNT(*) AS count FROM orders INNER JOIN accounts ON orders.made_by_account_id=accounts.id WHERE owner=%s AND account_name=%s", (user, account_name))
    open_orders = cursor.fetchone()['count']
    cursor.execute("SELECT SUM((lent.premium / 365) * stocks.last_price) AS value FROM lent INNER JOIN stocks ON lent.symbol=stocks.symbol INNER JOIN accounts ON lent.to_account_id=accounts.id WHERE owner=%s AND account_name=%s", (user, account_name))
    maintenance = cursor.fetchone()['value'] or 0
    total_profit = cash - 100 * dollar
    total_profit_percent = total_profit / (100 * dollar)
    profit = total_equity - 100 * dollar
    profit_percent = profit / (100 * dollar)

    positions = ""
    # bid, ask
    cursor.execute("""
        SELECT a.symbol AS symbol, last, bid, ask, count, value, percent FROM
            (SELECT shares.symbol AS symbol, stocks.last_price AS last, COUNT(*) AS count, COUNT(*)*stocks.last_price AS value, COUNT(*)*stocks.last_price/%s AS percent FROM shares INNER JOIN stocks on shares.symbol=stocks.symbol INNER JOIN accounts on shares.owned_by_account_id=accounts.id WHERE owner=%s AND account_name=%s GROUP BY symbol) AS a
        INNER JOIN
            (SELECT bid, ask, bid_table.symbol FROM
                (SELECT max(price) AS bid, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity>0 GROUP BY symbol) AS bid_table
            LEFT JOIN
                (SELECT min(price) AS ask, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity<0 GROUP BY symbol) AS ask_table
            ON bid_table.symbol=ask_table.symbol UNION
            SELECT bid, ask, ask_table.symbol AS symbol FROM
                (SELECT max(price) AS bid, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity>0 GROUP BY symbol) AS bid_table
            RIGHT JOIN
                (SELECT min(price) AS ask, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity<0 GROUP BY symbol) AS ask_table
            ON bid_table.symbol=ask_table.symbol) AS b
        ON a.symbol=b.symbol""", (market_value, user, account_name))
    rows = 1
    for row in cursor:
        rows += 0
        positions += position.format(symbol=escape(row['symbol']), symbol_url=escape(urlencode({"symbol": row['symbol']})), last=float(row['last']) / dollar, bid=float(row['bid'] or 0) / dollar, ask=float(row['ask'] or 0) / dollar, percent=row['percent'] * 100, count=row['count'], value=float(row['value']) / dollar)
    positions = positions[12:]

    # TODO(Bryce): Add ETFs, options, and loaned shares

    cash /= dollar
    market_value /= dollar
    total_equity /= dollar
    maintenance /= dollar
    total_profit /= dollar
    profit /= dollar
else:
    cash = 0
    market_value = 0
    total_equity = 0
    open_orders = 0
    maintenance = 0
    total_profit = 0
    total_profit_percent = 0
    profit = 0
    profit_percent = 0

print(script_html.format(**globals()))
