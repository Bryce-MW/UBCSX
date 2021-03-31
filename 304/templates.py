#! /bin/false

account_dropdown = """                <li><a href="main.py?{account_escaped}" data-selected="{selected}">{account}</a></li>\n"""
option_value = """        <option value="{value}"></option>\n"""
position = """            <span><a href="symbols.py?{symbol_url}">{symbol}</a></span>
            <span>${last:.2f}</span>
            <span>{bid}</span>
            <span>{ask}</span>
            <span>${value:.2f}</span>
            <span>{percent:.2f}%</span>
            <span>{count}</span>
            """
search_result = """            <span><a href="symbols.py?{symbol_url}">{symbol}</a></span>
            <span><a href="symbols.py?{symbol_url}">{name}</a></span>
            <span>{last}</span>
            <span>{bid}</span>
            <span>{ask}</span>
            """
order = """            <span><a href="symbols.py?{symbol_url}">{symbol}</a></span>
            <span>{type}</span>
            <span>${limit}</span>
            <span>${stop}</span>
            <span>${price}</span>
            <button aria-label="delete-{id}" form="delete-order-form" type="submit"
            name="delete" value="{id}"><span>Delete</span></button>
"""
symbol_order = """            <span class="head">{type}</span>
            <span class="head">{buy_sell}</span>
            <span class="head">{limit}</span>
            <span class="head">{count}</span>
            """
order = """            <span><a href="symbols.py?{symbol_url}">{symbol}</a></span>
            <span>{type}</span>
            <span>${limit}</span>
            <span>${stop}</span>
            <span>${price}</span>
            <span><button aria-label="delete-{id}" form="delete-order-form" type="submit"
            name="delete" value="{id}">Delete</span>
"""
