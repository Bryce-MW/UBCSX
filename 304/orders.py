#! /usr/bin/python3
from ubcsx import script_html, cursor, names, symbols, current_page, params, unescape, post

if "account" in params:
    account_name = unescape(params["account"][0])
    if not post:
        print(script_html.format(**globals()))
    else:
        print(post)

    # cursor.execute("""
    #         SELECT a.symbol AS symbol, last, bid, ask, count, value, percent FROM
    #             (SELECT shares.symbol AS symbol, stocks.last_price AS last, COUNT(*) AS count, COUNT(*)*stocks.last_price AS value, COUNT(*)*stocks.last_price/%s AS percent FROM shares INNER JOIN stocks on shares.symbol=stocks.symbol INNER JOIN accounts on shares.owned_by_account_id=accounts.id WHERE owner=%s AND account_name=%s GROUP BY symbol) AS a
    #         INNER JOIN
    #             (SELECT bid, ask, bid_table.symbol FROM
    #                 (SELECT max(price) AS bid, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity>0 GROUP BY symbol) AS bid_table
    #             LEFT JOIN
    #                 (SELECT min(price) AS ask, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity<0 GROUP BY symbol) AS ask_table
    #             ON bid_table.symbol=ask_table.symbol UNION
    #             SELECT bid, ask, ask_table.symbol AS symbol FROM
    #                 (SELECT max(price) AS bid, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity>0 GROUP BY symbol) AS bid_table
    #             RIGHT JOIN
    #                 (SELECT min(price) AS ask, symbol FROM `limit` INNER JOIN orders ON `limit`.order_id=orders.id WHERE orders.quantity<0 GROUP BY symbol) AS ask_table
    #             ON bid_table.symbol=ask_table.symbol) AS b
    #         ON a.symbol=b.symbol""", (market_value, user, account_name))
    # for row in cursor:
    #     rows += 0
    #     positions += position.format(symbol=escape(row['symbol']),
    #                                  symbol_url=escape(urlencode({"symbol": row['symbol']})),
    #                                  last=float(row['last']) / dollar, bid=format_ba(row['bid']),
    #                                  ask=format_ba(row['ask']), percent=row['percent'] * 100, count=row['count'],
    #                                  value=float(row['value']) / dollar)
    # positions = positions[12:]
else:
    print("Error: account name not provided")
