-- net_value_of_securities: Calculate the net value of securities (BUY - SELL)
SELECT
    (SELECT COALESCE(SUM(at.total), 0) 
     FROM asset_transaction at 
     JOIN transaction_type tt ON at.transaction_type_id = tt.id 
     WHERE tt.name LIKE '%buy%') -
    (SELECT COALESCE(SUM(at.total), 0) 
     FROM asset_transaction at 
     JOIN transaction_type tt ON at.transaction_type_id = tt.id 
     WHERE tt.name LIKE '%sell%') AS net_value;


-- total_value_of_securities: Calculate the total value of securities by symbol
SELECT symbol, SUM(total) AS total_value FROM asset_transaction GROUP BY symbol;


-- total_value_of_dividends: Calculate the total value of dividends
SELECT SUM(at.amount) AS total_dividends 
FROM asset_transaction at
JOIN transaction_type tt ON at.transaction_type_id = tt.id 
WHERE tt.name = 'dividend';


-- total_value_of_dividends_by_symbol: Calculate the total value of dividends by symbol
SELECT at.symbol, SUM(at.amount) AS total_dividends 
FROM asset_transaction at
JOIN transaction_type tt ON at.transaction_type_id = tt.id 
WHERE tt.name = 'dividend'
GROUP BY at.symbol;


-- net_ticker_summary: Calculate the net average price of securities by symbol
SELECT
    ai.symbol,
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
    asset_info ai
    LEFT JOIN (
        SELECT
            at.asset_id,
            SUM(at.quantity) AS total_buy_qty,
            SUM(at.total) AS total_buy_amnt
        FROM
            asset_transaction at
            JOIN asset_info ai ON at.asset_id = ai.id
            JOIN transaction_type tt ON at.transaction_type_id = tt.id
        WHERE
            ai.symbol = ?
            AND tt.name LIKE '%buy%'
        GROUP BY at.asset_id
    ) AS buy ON ai.id = buy.asset_id
    LEFT JOIN (
        SELECT
            at.asset_id,
            AVG(at.avg_price) AS avg_sell_price,
            SUM(at.quantity) AS total_sell_qty,
            SUM(at.total) AS total_sell_amnt
        FROM
            asset_transaction at
            JOIN asset_info ai ON at.asset_id = ai.id
            JOIN transaction_type tt ON at.transaction_type_id = tt.id
        WHERE
            ai.symbol = ?
            AND tt.name LIKE '%sell%'
        GROUP BY at.asset_id
    ) AS sell ON ai.id = sell.asset_id
    LEFT JOIN (
        SELECT
            at.asset_id,
            SUM(at.total) AS total_divs
        FROM
            asset_transaction at
            JOIN asset_info ai ON at.asset_id = ai.id
            JOIN transaction_type tt ON at.transaction_type_id = tt.id
        WHERE
            ai.symbol = ?
            AND tt.name = 'dividend'
        GROUP BY at.asset_id
    ) AS div ON ai.id = div.asset_id;


-- view_current_portfolio: Select the entire current portfolio holdings
SELECT
    symbol,
    total_buy_qty,
    total_buy_amnt,
    avg_buy_price,
    total_sell_qty,
    total_sell_amnt,
    avg_sell_price,
    total_divs,
    net_qty,
    net_value,
    net_avg_price,
    break_even_value
FROM (
    SELECT
        buy.symbol,
        buy.total_buy_qty,
        buy.total_buy_amnt,
        ROUND((buy.total_buy_amnt / buy.total_buy_qty), 2) AS avg_buy_price,
        COALESCE(sell.total_sell_qty, 0) AS total_sell_qty,
        COALESCE(sell.total_sell_amnt, 0) AS total_sell_amnt,
        ROUND((COALESCE(sell.total_sell_amnt, 0) / COALESCE(sell.total_sell_qty, 1)), 2) AS avg_sell_price,
        div.total_divs,
        (buy.total_buy_qty - COALESCE(sell.total_sell_qty, 0)) AS net_qty,
        ROUND(buy.total_buy_amnt - COALESCE(sell.total_sell_amnt, 0), 2) AS net_value,
        ROUND(((buy.total_buy_amnt - COALESCE(sell.total_sell_amnt, 0)) / (buy.total_buy_qty - COALESCE(sell.total_sell_qty, 0))), 2) AS net_avg_price,
        ROUND((buy.total_buy_amnt - COALESCE(sell.total_sell_amnt, 0) - div.total_divs), 2) AS break_even_value
    FROM (
        SELECT
            at.symbol,
            SUM(quantity) AS total_buy_qty,
            SUM(total) AS total_buy_amnt
        FROM
            asset_transaction at
        JOIN transaction_type tt ON at.transaction_type_id = tt.id
        WHERE
            tt.name LIKE '%buy%'
        GROUP BY
            at.symbol
    ) AS buy
    LEFT JOIN (
        SELECT
            at.symbol,
            AVG(avg_price) AS avg_sell_price,
            SUM(quantity) AS total_sell_qty,
            SUM(total) AS total_sell_amnt
        FROM
            asset_transaction at
        JOIN transaction_type tt ON at.transaction_type_id = tt.id
        WHERE
            tt.name LIKE '%sell%'
        GROUP BY
            at.symbol
    ) AS sell ON buy.symbol = sell.symbol
    LEFT JOIN (
        SELECT
            at.symbol,
            SUM(amount) AS total_divs
        FROM
            asset_transaction at
        JOIN transaction_type tt ON at.transaction_type_id = tt.id
        WHERE
            tt.name = 'dividend'
        GROUP BY
            at.symbol
    ) AS div ON buy.symbol = div.symbol
) AS result
WHERE
    net_qty <> 0;
