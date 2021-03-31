#! /usr/bin/python3
from templates import order
from ubcsx import script_html, cursor, names, symbols, current_page, params, unescape, post, user, escape, urlencode, dollar

orders = ""
rows = 0

if "account" in params:
    account_name = unescape(params["account"][0])
    if not post:
        # cursor.execute()
        # for row in cursor:
        #     # rows += 0
        #     orders += order.format(symbol=escape(row['symbol']),
        #                            symbol_url=escape(urlencode({"symbol": row['symbol']})),
        #                            type=row['type'],
        #                            limit=float(row['limit']) / dollar if (row['type'] == 'Limit') else "",
        #                            stop=float(row['stop']) / dollar if (row['type'] == 'Stop') else "",
        #                            price=float(row['value']) / dollar,
        #                            id=row['id'])
        rows += 1
        orders += order.format(symbol="AAPL",
                                   symbol_url=escape(urlencode({"symbol": "AAPL"})),
                                   type="Limit",
                                   limit=float("3245345") / dollar if ("Limit" == 'Limit') else "",
                                   stop=float("3245345") / dollar if ("Limit" == 'Stop') else "",
                                   price=float("3245345") / dollar,
                               id=1)
        orders = orders[12:]
        print(script_html.format(**globals()))
    else:
        print(post)


else:
    print("Error: account name not provided")
