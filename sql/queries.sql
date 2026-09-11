
-- Query 1: Top 5 Funds by AUM
SELECT
    f.scheme_name,
    f.fund_house,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;


-- Query 2: Average NAV per Month
SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 2) AS average_nav
FROM fact_nav
GROUP BY strftime('%Y-%m', date)
ORDER BY month;


-- Query 3: SIP Year-over-Year Growth
WITH yearly_sip AS (
    SELECT
        strftime('%Y', transaction_date) AS year,
        SUM(amount_inr) AS total_sip_amount
    FROM fact_transactions
    WHERE transaction_type = 'SIP'
    GROUP BY strftime('%Y', transaction_date)
)
SELECT
    year,
    ROUND(total_sip_amount, 2) AS total_sip_amount,
    ROUND(
        (
            total_sip_amount -
            LAG(total_sip_amount) OVER (ORDER BY year)
        ) * 100.0 /
        LAG(total_sip_amount) OVER (ORDER BY year),
        2
    ) AS yoy_growth_pct
FROM yearly_sip
ORDER BY year;


-- Query 4: Transactions by State
SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_transaction_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transaction_amount DESC;


-- Query 5: Funds with Expense Ratio Below 1%
SELECT
    scheme_name,
    fund_house,
    category,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct ASC;


-- Query 6: Top 5 Funds by 5-Year Return
SELECT
    f.scheme_name,
    f.fund_house,
    p.return_5yr_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
WHERE p.return_5yr_pct IS NOT NULL
ORDER BY p.return_5yr_pct DESC
LIMIT 5;


-- Query 7: Transaction Amount by Transaction Type
SELECT
    transaction_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;


-- Query 8: Top 5 Fund Houses by AUM
SELECT
    fund_house,
    ROUND(SUM(aum_crore), 2) AS total_aum_crore,
    SUM(num_schemes) AS total_schemes
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC
LIMIT 5;


-- Query 9: Average Transaction Amount by Payment Mode
SELECT
    payment_mode,
    COUNT(*) AS total_transactions,
    ROUND(AVG(amount_inr), 2) AS average_transaction_amount
FROM fact_transactions
GROUP BY payment_mode
ORDER BY average_transaction_amount DESC;


-- Query 10: Top 5 Funds by Sharpe Ratio
SELECT
    f.scheme_name,
    f.fund_house,
    p.sharpe_ratio,
    p.return_3yr_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
WHERE p.sharpe_ratio IS NOT NULL
ORDER BY p.sharpe_ratio DESC
LIMIT 5;
