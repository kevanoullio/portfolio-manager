-- Query 1: Calculate the net value of securities (BUY - SELL)
SELECT 
    (SELECT COALESCE(SUM(total), 0) FROM security WHERE type LIKE '%BUY%') -
    (SELECT COALESCE(SUM(total), 0) FROM security WHERE type LIKE '%SELL%') AS net_value;


-- Query 2: Calculate the total value of securities by symbol
SELECT symbol, SUM(total) AS total_value FROM security GROUP BY symbol;


-- Query 3: Calculate the total value of dividends
SELECT SUM(amount) AS total_dividends FROM dividend;


-- Query 4: Calculate the total value of dividends by symbol
SELECT symbol, SUM(amount) AS total_dividends FROM dividend GROUP BY symbol;


-- net_ticker_summary: Calculate the net average price of securities by symbol
SELECT
    '?' AS symbol,
    buy.total_buy_qty,
    buy.total_buy_amnt,
    ROUND((buy.total_buy_amnt / buy.total_buy_qty), 2) AS avg_buy_price,
    COALESCE(sell.total_sell_qty, 0) AS total_sell_qty,
    COALESCE(sell.total_sell_amnt, 0) AS total_sell_amnt,
    ROUND((COALESCE(sell.total_sell_amnt, 0) / COALESCE(sell.total_sell_qty, 1)), 2) AS avg_sell_price,
    div.total_divs,
    (buy.total_buy_qty - COALESCE(sell.total_sell_qty, 0)) AS net_qty,
    buy.total_buy_amnt - COALESCE(sell.total_sell_amnt, 0) AS net_value,
    ROUND(((buy.total_buy_amnt - COALESCE(sell.total_sell_amnt, 0)) / (buy.total_buy_qty - COALESCE(sell.total_sell_qty, 0))), 2) AS net_avg_price,
    buy.total_buy_amnt - COALESCE(sell.total_sell_amnt, 0) - div.total_divs AS break_even_value
FROM
    (
        SELECT
            SUM(quantity) AS total_buy_qty,
            SUM(total) AS total_buy_amnt
        FROM
            security
        WHERE
            symbol = '?'
            AND type LIKE '%BUY%'
    ) AS buy,
    (
        SELECT
            AVG(avg_price) AS avg_sell_price,
            SUM(quantity) AS total_sell_qty,
            SUM(total) AS total_sell_amnt
        FROM
            security
        WHERE
            symbol = '?'
            AND type LIKE '%SELL%'
    ) AS sell,
    (
        SELECT
            SUM(amount) AS total_divs
        FROM
            dividend
        WHERE
            symbol = '?'
    ) AS div;
