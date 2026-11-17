-- Customer Shopping Dashboard | MySQL / phpMyAdmin
-- Source table: customer. Source amount field: purchase_amt.

-- Q1. Revenue by gender
SELECT gender, SUM(purchase_amt) AS total_revenue FROM customer GROUP BY gender ORDER BY total_revenue DESC;

-- Q2. Discounted purchases strictly above the overall average
SELECT customer_id, item_purchased, category, purchase_amt FROM customer
WHERE discount_applied = 'Yes' AND purchase_amt > (SELECT AVG(purchase_amt) FROM customer)
ORDER BY purchase_amt DESC;

-- Q3. Five products with the highest average review rating
SELECT item_purchased, ROUND(AVG(CAST(review_rating AS DECIMAL(3,1))),2) AS average_product_rating,
       COUNT(*) AS purchase_count
FROM customer GROUP BY item_purchased ORDER BY average_product_rating DESC, purchase_count DESC LIMIT 5;

-- Q4. Standard versus Express shipping spend
SELECT shipping_type, ROUND(AVG(purchase_amt),2) AS average_purchase_amount, COUNT(*) AS purchase_count
FROM customer WHERE shipping_type IN ('Standard','Express') GROUP BY shipping_type;

-- Q5. Subscriber versus non-subscriber spend
SELECT subscription_status, COUNT(*) AS total_customers, ROUND(AVG(purchase_amt),2) AS average_spend,
       ROUND(SUM(purchase_amt),2) AS total_revenue
FROM customer GROUP BY subscription_status ORDER BY total_revenue DESC;

-- Q6. Five products with the greatest discounted-purchase share
SELECT item_purchased, ROUND(100.0 * AVG(discount_applied = 'Yes'),2) AS discount_rate_pct,
       COUNT(*) AS purchase_count
FROM customer GROUP BY item_purchased ORDER BY discount_rate_pct DESC, purchase_count DESC LIMIT 5;

-- Q7. Customer loyalty segments
SELECT CASE WHEN previous_purchases = 1 THEN 'New' WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
            ELSE 'Loyal' END AS customer_segment,
       COUNT(*) AS customer_count, ROUND(SUM(purchase_amt),2) AS total_revenue
FROM customer GROUP BY customer_segment ORDER BY FIELD(customer_segment,'New','Returning','Loyal');

-- Q8. Top three products within each category by revenue
WITH product_revenue AS (
  SELECT category, item_purchased, SUM(purchase_amt) AS total_revenue, COUNT(*) AS purchase_count,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(purchase_amt) DESC, item_purchased) AS category_rank
  FROM customer GROUP BY category, item_purchased
)
SELECT category, item_purchased, total_revenue, purchase_count, category_rank FROM product_revenue
WHERE category_rank <= 3 ORDER BY category, category_rank;

-- Q9. Subscription rate by buyer type
SELECT CASE WHEN previous_purchases > 1 THEN 'Repeat buyer' ELSE 'First-time buyer' END AS buyer_type,
       COUNT(*) AS customer_count, SUM(subscription_status = 'Yes') AS subscribers,
       ROUND(100.0 * AVG(subscription_status = 'Yes'),2) AS subscription_rate_pct
FROM customer GROUP BY buyer_type ORDER BY FIELD(buyer_type,'First-time buyer','Repeat buyer');

-- Q10. Revenue and spend by age group
SELECT age_group, COUNT(*) AS customer_count, ROUND(SUM(purchase_amt),2) AS total_revenue,
       ROUND(AVG(purchase_amt),2) AS average_spend
FROM customer GROUP BY age_group ORDER BY total_revenue DESC;

-- Q11. Category-season revenue opportunity
SELECT category, season, COUNT(*) AS purchase_count, ROUND(SUM(purchase_amt),2) AS total_revenue,
       ROUND(AVG(purchase_amt),2) AS average_spend
FROM customer GROUP BY category, season ORDER BY total_revenue DESC;

-- Q12. Shipping experience: volume, revenue, spend, rating
SELECT shipping_type, COUNT(*) AS purchase_count, ROUND(SUM(purchase_amt),2) AS total_revenue,
       ROUND(AVG(purchase_amt),2) AS average_spend, ROUND(AVG(CAST(review_rating AS DECIMAL(3,1))),2) AS average_rating
FROM customer GROUP BY shipping_type ORDER BY total_revenue DESC;
