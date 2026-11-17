# Analysis notes

## Query corrections

- The supplied dataset uses `purchase_amt`, not `purchase_amount`.
- Q2 uses `>` rather than `>=` because “more than average” excludes values equal to the average.
- Q3 explicitly casts review ratings for MySQL compatibility.
- Q6 calculates a rate with `AVG(discount_applied = 'Yes')`; ranking only by discount count would favor high-volume products.
- Q7 treats `previous_purchases = 1` as New, 2–10 as Returning, and 11+ as Loyal. There are no zero prior-purchase records in this dataset.
- Q9 compares subscription *rates* rather than raw subscriber totals, which avoids a group-size bias.

## Interpretation caution

Discount incidence is descriptive, not causal. A high percentage of discounted purchases does not mean that a discount increased demand without a comparison design.
