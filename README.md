# Customer Shopping Analysis

An interview-ready analytics portfolio built from a 3,900-record customer shopping dataset. It contains six clear charts, corrected SQL queries, and the original Python-to-MySQL loading script.

## Charts

| Chart | What it answers |
| --- | --- |
| Revenue by gender | Which gender generated more revenue? |
| Revenue by category | Which product category contributes the most revenue? |
| Revenue by age group | How does revenue vary by age segment? |
| Subscription mix | What share of customers are subscribers? |
| Discount rate by product | Which products are most often bought with a discount? |
| Average spend by shipping type | How do Express and Standard orders compare? |

Open any file in the charts folder to view a ready-to-present SVG chart.

## Project structure

- charts/ — six interview-ready chart files
- scripts/customer.py — original Python loader
- docs/ — analysis notes and query corrections
- sql/ — MySQL / phpMyAdmin query set

## Run the original Python loader

1. Put the raw input CSV beside the folder where you run the script and name it `customer_shopping_behavior.csv`.
2. Install requirements: `pip install -r requirements.txt`.
3. Run: `python scripts/customer.py`.
4. Use the SQL file in phpMyAdmin after the data loads.

## Interview takeaway

The charts are intentionally simple: one question per chart, readable labels, and a short narrative that does not overstate what the data proves.
