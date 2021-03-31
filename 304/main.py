#! /usr/bin/python3
from templates import account_dropdown, position
from ubcsx import cursor, dollar, escape, params, script_html, unescape, urlencode, user, current_page, names, symbols, format_ba, redirect


all_selected = False
if "all" in params:
    all_selected = True


if "account" not in params:
    account_name = ""
else:
    account_name = unescape(params["account"][0])

cursor.execute("SELECT account_name FROM accounts WHERE owner=%s", (user,))
accounts = ""
account_list = []
for account in cursor:
    account_list.append(account["account_name"])
    accounts += account_dropdown.format(account=escape(account["account_name"]), account_escaped=urlencode({"account": account["account_name"]}), selected=account["account_name"] == account_name)
accounts = accounts[16:]

if account_name not in account_list and not all_selected:
    redirect("main.py?" + urlencode({"account":account_list[0]}))
    exit()

rows = 1
positions = ""

if "account" in params:
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
    for row in cursor:
        rows += 0
        account = params["account"][0] if "account" in params else ""
        symbol_url = escape(urlencode({"symbol":row['symbol'], "account":account}))
        positions += position.format(symbol=escape(row['symbol']), symbol_url=escape(symbol_url), last=float(row['last']) / dollar, bid=format_ba(row['bid']), ask=format_ba(row['ask']), percent=row['percent'] * 100, count=row['count'], value=float(row['value']) / dollar)
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
    if all_selected:
        cursor.execute("""
            SELECT a.symbol AS symbol, last, bid, ask, 0 AS count, 0 AS value, 0 AS percent FROM
                (SELECT
                    stocks.symbol AS symbol,
                    stocks.last_price AS last
                FROM
                    stocks
                WHERE
                    NOT EXISTS (SELECT 1 FROM accounts WHERE accounts.owner=%(owner)s AND NOT EXISTS (SELECT 1 FROM shares WHERE shares.owned_by_account_id=accounts.id AND shares.symbol=stocks.symbol))
                ) AS a
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
            ON a.symbol=b.symbol""", {"owner":user})
        for row in cursor:
            rows += 0
            account = params["account"][0] if "account" in params else ""
            symbol_url = urlencode({"symbol":row['symbol'], "account":account})
            positions += position.format(symbol=escape(row['symbol']), symbol_url=symbol_url, last=float(row['last']) / dollar, bid=format_ba(row['bid']), ask=format_ba(row['ask']), percent=row['percent'] * 100, count=row['count'], value=float(row['value']) / dollar)
        positions = positions[12:]


print(script_html.format(**globals()))
