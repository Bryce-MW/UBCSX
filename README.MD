# UBCSX: The UBC Stock Exchange

The purpose of this project is to model a stock exchange in a way which ensures that all securities are accounted for. 
We will be implementing stocks and American-style options which can be held by accounts and traded by putting in 
market, limit, and stop orders. We also allow for the lending of shares though the lending system is simplified 
compared to the purchasing system. There is also a simplification of ETFs.

In this simplification, buying into an ETF deposits money into the account linked with the ETF and entitles you to 
units of the ETF depending on the percentage of the new total market value which you put in and the current total 
number of units. When you sell, you will be entitled to your share of the market value based on how many units you are 
selling and how many total units exist. If there is not enough balance, shares will be automatically sold at market 
price depending on their default sort order.

There are some limitations to this model. In this model, everyone directly controls accounts with the exchanges, there 
are no brokers, clearinghouses, or market-makers. All shares are controlled by the exchange rather than only being 
traded by the exchange. I consider this a benefit because it means that fake shares, naked shorts, and failure to 
deliver are less likely or impossible to happen.

Our application will run using Python and MySQL, likely as a web application. Our application will allow users to 
create an account which has a starting balance. Users with accounts can IPO companies, enter buy and sell orders for 
shares and options, borrow or lend out shares, and create an ETF associated with their account. One user may have 
multiple accounts. We have not yet decided on how users will be authenticated (we may not do authentication for 
demonstration purposes).

![ER Diagram](images/ER.png)

Note that Orders has two ISA relationships. Formally: StockOrder AND OptionOrder COVER Orders. Market AND Limit AND 
Stop COVER Order. To be clear, an order must be exactly two things, one of StockOrder or OptionOrder (but not both) and 
it must also be one of Market, Limit, or Stop. This means that an order could be both a StockOrder and Market but it 
could not be Market and Limit or SockOrder and OptionOrder and Stop. In the diagram, I modelled this by using two 
independent ISA relationships which each have total participation by the Orders entity.
