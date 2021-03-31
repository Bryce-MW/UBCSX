#! /usr/bin/python3
from templates import search_result
from ubcsx import names, symbols, script_html, params, current_page, urlencode, cursor, escape, format_ba, dollar

search_results = ""
rows = 0

query = params["q"][0] if "q" in params else ""
query_url = urlencode({"query":query})

if query:
    cursor.execute("""
        SELECT a.symbol AS symbol, a.name AS name, last, bid, ask FROM
            (SELECT stocks.symbol AS symbol, stocks.name AS name, stocks.last_price AS last FROM stocks WHERE symbol LIKE CONCAT('%', %(q)s, '%') OR name LIKE CONCAT('%', %(q)s, '%')) AS a
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
        ON a.symbol=b.symbol
        ORDER BY a.symbol LIKE CONCAT(%(q)s, '%'), a.name LIKE CONCAT(%(q)s, '%'), a.symbol LIKE CONCAT('%', %(q)s, '%'), a.name LIKE CONCAT('%', %(q)s, '%'), a.symbol
        """, {"q":query})

    for row in cursor:
        rows += 1
        account = params["account"][0] if "account" in params else ""
        symbol_url = urlencode({"symbol":row['symbol'], "account":account})
        search_results += search_result.format(symbol_url=symbol_url, symbol=escape(row["symbol"]), name=escape(row["name"]), last=format_ba(row["last"]), bid=format_ba(row["bid"]), ask=format_ba(row["ask"]))

    cursor.execute("""
        SELECT etfs.symbol AS symbol, accounts.account_name AS name, (IFNULL(SUM(stocks.last_price), 0) + accounts.balance) / IFNULL((SELECT SUM(units) FROM owns AS o2 where o2.symbol=etfs.symbol), 1) AS last
        FROM etfs INNER JOIN accounts ON accounts.id=etfs.controls_account_id LEFT JOIN shares ON accounts.id=shares.owned_by_account_id LEFT JOIN stocks ON shares.symbol=stocks.symbol
        GROUP BY etfs.symbol, accounts.account_name
        HAVING etfs.symbol LIKE CONCAT('%', %(q)s, '%') OR accounts.account_name LIKE CONCAT('%', %(q)s, '%')
        ORDER BY etfs.symbol LIKE CONCAT(%(q)s, '%') DESC, accounts.account_name LIKE CONCAT(%(q)s, '%') DESC, etfs.symbol LIKE CONCAT('%', %(q)s, '%') DESC, accounts.account_name LIKE CONCAT('%', %(q)s, '%') DESC, etfs.symbol
        """, {"q":query})

    for row in cursor:
        rows += 1
        search_results += search_result.format(symbol_url=urlencode({"symbol": row['symbol']}), symbol=escape(row["symbol"]), name=escape(row["name"]), last=format_ba(row["last"]), bid="", ask="")


print(script_html.format(**globals()))