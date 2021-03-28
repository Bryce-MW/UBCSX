#! /usr/bin/python3
from ubcsx import script_html, names, symbols, current_page, params

symbol = params["symbol"] if "symbol" in params else ""


print(script_html.format(**globals()))