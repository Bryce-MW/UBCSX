#! /usr/bin/python3
from ubcsx import script_html, user, redirect, post, cursor, escape, unescape, urlencode, current_page, params
from templates import account_dropdown, option_value

cursor.execute("SELECT account_name FROM accounts WHERE owner=%s", (user,))
accounts = ""
for account in cursor:
    accounts += account_dropdown.format(account=escape(account["account_name"]), account_escaped=urlencode({"account":account["account_name"]}))
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
    cursor.execute("SELECT balance FROM accounts WHERE owner=%s AND account_name=%s", (user,account_name))
    cash = cursor.fetchone()["balance"]
    cursor.execute("SELECT SUM(stocks.last_price) AS value FROM shares INNER JOIN stocks ON shares.symbol=stocks.symbol INNER JOIN accounts ON accounts.id=shares.owned_by_account_id WHERE owner=%(user)s AND account_name=%(account)s", {"user":user, "account":account_name})
    market_value = cursor.fetchone()['value'] or 0
    cursor.execute("SELECT SUM((stocks.last_price + accounts.balance) / (owns.units / (SELECT SUM(units) FROM owns AS o2 where o2.symbol=owns.symbol))) AS value FROM shares INNER JOIN stocks ON shares.symbol=stocks.symbol INNER JOIN accounts ON accounts.id=shares.owned_by_account_id INNER JOIN etfs ON accounts.id=etfs.controls_account_id INNER JOIN owns ON owns.symbol=etfs.symbol INNER JOIN accounts AS a2 ON a2.id=owns.account_id WHERE a2.owner=%(user)s AND a2.account_name=%(account)s", {"user":user, "account":account_name})
    market_value += cursor.fetchone()['value'] or 0
    total_equity = cash + market_value
    cursor.execute("SELECT COUNT(*) AS count FROM orders INNER JOIN accounts ON orders.made_by_account_id=accounts.id WHERE owner=%s AND account_name=%s", (user,account_name))
    open_orders = cursor.fetchone()['count']
    cursor.execute("SELECT SUM((lent.premium / 365) * stocks.last_price) AS value FROM lent INNER JOIN stocks ON lent.symbol=stocks.symbol INNER JOIN accounts ON lent.to_account_id=accounts.id WHERE owner=%s AND account_name=%s", (user,account_name))
    maintenance = cursor.fetchone()['value'] or 0
    total_profit = cash - 1000000
    total_profit_percent = total_profit / 1000000
    profit = total_equity - 1000000
    profit_percent = profit / 1000000

    cash /= 10000
    market_value /= 10000
    total_equity /= 10000
    maintenance /= 10000
    total_profit /= 10000
    profit /= 10000
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