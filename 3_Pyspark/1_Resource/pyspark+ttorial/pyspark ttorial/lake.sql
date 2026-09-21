-- 02_sales_summary.sql
CREATE OR REPLACE TABLE devlopment.lake.sales_orders_agg AS
SELECT
    region,
    DATE_TRUNC('month', order_date) AS sales_month,
    SUM(amount) AS total_sales,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM devlopment.lake.sales_orders
GROUP BY region, DATE_TRUNC('month', order_date);
