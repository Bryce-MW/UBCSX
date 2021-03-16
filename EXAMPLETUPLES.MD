# Example Tuples

This file provides 5 example tuples for each table created by the schema as described in `schema.ddl`

lendables
| id | input_datetime       | premium | symbol | share_id | account_id |
|----|----------------------|---------|--------|----------|------------|
| 1  | 2021-03-01  02:30:26 | 0.12    | AAPL   | 1        | 1          |
| 2  | 2021-03-02  11:23:42 | 0.05    | GOOGL  | 2        | 2          |
| 3  | 2021-02-22  23:12:32 | 0.2     | MSFT   | 3        | 3          |
| 4  | 2021-02-15  06:43:13 | 0.23    | BBY    | 4        | 4          |
| 5  | 2021-01-24  17:52:52 | 0.01    | AMZN   | 5        | 4          |

lent
| id | premium | share_id | symbol | by_account_id | to_account_id |
|----|---------|----------|--------|---------------|---------------|
| 1  | 0.34    | 1        | AAPL   | 1             | 2             |
| 2  | 0.1     | 2        | GOOGL  | 2             | 3             |
| 3  | 0.5     | 3        | MSFT   | 3             | 5             |
| 4  | 0.23    | 4        | BBY    | 4             | 1             |
| 5  | 0.01    | 5        | AMZN   | 4             | 2             |

shares
| id | symbol | owned_by_account_id |
|----|--------|---------------------|
| 1  | AAPL   | 2                   |
| 2  | GOOGL  | 3                   |
| 3  | MSFT   | 4                   |
| 4  | BBY    | 1                   |
| 5  | AMZN   | 2                   |

accounts
| id | balance    | owner    |
|----|------------|----------|
| 1  | 1983209    | ahjkd34  |
| 2  | 1239023    | john143  |
| 3  | 3049283    | orange1  |
| 4  | 23904805   | terryl23 |
| 5  | 1230948233 | d9sk4    |

owns
| symbol | account_id | units |
|--------|------------|-------|
| ARKK   | 1          | 13    |
| SPY    | 3          | 26    |
| ICLN   | 2          | 32    |
| TQQQ   | 4          | 16    |
| GLD    | 5          | 58    |

etfs
| symbol | controls_account_id |
|--------|---------------------|
| ARKK   | 1                   |
| TQQQ   | 4                   |
| ICLN   | 2                   |
| SPY    | 3                   |
| GLD    | 5                   |

stocks
| last_price | name      | symbol |
|------------|-----------|--------|
| 142        | Apple     | AAPL   |
| 156        | Google    | GOOGL  |
| 65         | Microsoft | MSFT   |
| 102        | Best Buy  | BBY    |
| 204        | Amazon    | AMZN   |

orders
| id | input_datetime      | valid_until         | quantity | symbol | made_by_account_id |
|----|---------------------|---------------------|----------|--------|--------------------|
| 1  | 2021-02-02 15:40:33 | 2021-02-20 23:24:25 | 25       | AAPL   | 1                  |
| 2  | 2021-01-17 04:27:42 | 2021-02-02 18:28:39 | 343      | GOOGL  | 4                  |
| 3  | 2021-01-01 05:50:23 | 2021-01-25 10:54:23 | 123      | MSFT   | 3                  |
| 4  | 2021-02-01 16:17:47 | 2021-02-10 20:45:52 | 4567     | BBY    | 2                  |
| 5  | 2021-01-22 19:40:21 | 2021-02-06 08:58:40 | 3        | AMZN   | 5                  |

contracts
| id | expiration      | strike_price | symbol | written_by_account_id | owned_by_account_id |
|----|-----------------|--------------|--------|-----------------------|---------------------|
| 1  | 1/26/2021 5:53  | 362          | AAPL   | 1                     | 1                   |
| 2  | 1/20/2021 4:05  | 12378        | GOOGL  | 3                     | 2                   |
| 3  | 2/10/2021 14:16 | 5635         | MSFT   | 2                     | 3                   |
| 4  | 1/10/2021 20:19 | 9567         | BBY    | 4                     | 3                   |
| 5  | 2/1/2021 2:30   | 408          | AMZN   | 5                     | 5                   |

option_order
| strike_price | expiration      | order_id |
|--------------|-----------------|----------|
| 12345        | 1/4/2021 18:00  | 1        |
| 34324        | 1/27/2021 22:51 | 2        |
| 1623         | 2/26/2021 7:01  | 3        |
| 64342        | 2/2/2021 17:48  | 4        |
| 8349         | 1/31/2021 4:14  | 5        |

\`limit\`
| price | order_id |
|-------|----------|
| 142   | 1        |
| 23    | 2        |
| 1     | 3        |
| 65473 | 4        |
| 2354  | 5        |

stop
| price  | limit_price | order_id |
|--------|-------------|----------|
| 54336  | 7568        | 1        |
| 264574 | 43563       | 2        |
| 4563   | 987         | 3        |
| 9657   | 2346        | 4        |
| 457    | 1509        | 5        |
