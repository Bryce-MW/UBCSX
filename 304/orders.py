#! /usr/bin/python3
from ubcsx import script_html, names, symbols, current_page

print(script_html.format(**globals()))