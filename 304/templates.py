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
            <span>${last:.2f}</span>
            <span>{bid}</span>
            <span>{ask}</span>
            """
