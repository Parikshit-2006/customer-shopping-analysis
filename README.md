# Customer Shopping Analysis

An interview-ready analytics portfolio built from a 3,900-record customer shopping dataset. It contains polished charts, corrected SQL, and a Python-to-MySQL loading script—no Tableau project or website required.

## Charts

| Chart | What it answers |
| --- | --- |
| `charts/revenue_by_gender.svg` | Which gender generated more revenue? |
| `charts/revenue_by_category.svg` | Which product category contributes the most revenue? |
| `charts/revenue_by_age_group.svg` | How does revenue vary by age segment? |
| `charts/subscription_mix.svg` | What share of customers are subscribers? |
| `charts/discount_rate_by_product.svg` | Which products are most often purchased with a discount? |
| `charts/shipping_average_spend.svg` | How does average spend compare for Express and Standard shipping? |

Each chart has one plain-English title and can be opened directly in a browser, added to a presentation, or discussed during an interview.

## Highlights

- Six clear SVG charts generated directly from the raw dataset.
- Corrected MySQL queries for the original ten questions plus two useful additions.
- A MAMP/phpMyAdmin-compatible Python loader that reads connection settings from environment variables.

## Project structure

```text
.
├── charts/                    # Ready-to-present SVG chart files
├── scripts/load_customer_data.py
├── scripts/generate_charts.py
├── sql/customer_dashboard_queries.sql
├── docs/analysis-notes.md
├── data/README.md
├── requirements.txt
└── .env.example
```

## Regenerate the charts

1. Copy the dataset to `data/customer.csv`.
2. Run: `python scripts/generate_charts.py`.
3. Open the generated SVG files from the `charts/` folder.

## Load the dataset into MySQL

1. Copy the dataset to `data/customer.csv` (it is intentionally ignored by Git).
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` values into your terminal environment (or adjust them for your MySQL/MAMP setup).
4. Run `python scripts/load_customer_data.py`.
5. Run any query in `sql/customer_dashboard_queries.sql` through phpMyAdmin.

## Analytical notes

The dashboard figures are calculated from the supplied 3,900-record dataset. See [analysis notes](docs/analysis-notes.md) for the query corrections and interpretation cautions.

