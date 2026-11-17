"""Generate simple interview-ready SVG charts from customer.csv (no extra packages)."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

W, H, LEFT, RIGHT, TOP, BOTTOM = 960, 540, 205, 105, 88, 90
INK, MUTED, GRID, TEAL, CORAL, GOLD, PALE = "#14222a", "#617179", "#dedbd2", "#277d7b", "#e96846", "#f2bb49", "#92b8b6"


def svg(title: str, subtitle: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">{escape(title)}</title><desc id="d">{escape(subtitle)}</desc>
<rect width="100%" height="100%" fill="#fffdfa"/>
<text x="{LEFT}" y="45" font-family="Arial, sans-serif" font-size="27" font-weight="700" fill="{INK}">{escape(title)}</text>
<text x="{LEFT}" y="70" font-family="Arial, sans-serif" font-size="14" fill="{MUTED}">{escape(subtitle)}</text>{body}
</svg>'''


def bars(title: str, subtitle: str, pairs: list[tuple[str, float]], filename: str, suffix: str = "", color: str = TEAL) -> None:
    max_value = max(value for _, value in pairs)
    usable = W - LEFT - RIGHT
    row = 64
    body = []
    for i, (label, value) in enumerate(pairs):
        y = TOP + i * row
        width = usable * value / max_value
        body.append(f'<text x="{LEFT-14}" y="{y+22}" text-anchor="end" font-family="Arial" font-size="15" fill="{INK}">{escape(label)}</text>')
        body.append(f'<rect x="{LEFT}" y="{y}" width="{usable}" height="30" fill="#edf0ed"/>')
        body.append(f'<rect x="{LEFT}" y="{y}" width="{width:.1f}" height="30" fill="{color if i != 1 else CORAL}"/>')
        text = f"${value:,.0f}" if suffix == "$" else f"{value:,.2f}{suffix}" if suffix else f"{value:,.0f}"
        body.append(f'<text x="{LEFT+width+12:.1f}" y="{y+21}" font-family="Arial" font-size="14" font-weight="700" fill="{INK}">{text}</text>')
    (OUT / filename).write_text(svg(title, subtitle, "".join(body)), encoding="utf-8")


def donut(yes: int, no: int) -> None:
    pct = yes / (yes + no) * 100
    # A simple ring: the first arc is the subscriber share.
    import math
    cx, cy, r = 340, 285, 122
    angle = pct / 100 * 2 * math.pi
    endx, endy = cx + r * math.sin(angle), cy - r * math.cos(angle)
    large = 1 if pct > 50 else 0
    arc = f'M {cx} {cy-r} A {r} {r} 0 {large} 1 {endx:.1f} {endy:.1f}'
    body = f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PALE}" stroke-width="42"/>
<path d="{arc}" fill="none" stroke="{CORAL}" stroke-width="42"/>
<text x="{cx}" y="{cy-5}" text-anchor="middle" font-family="Arial" font-size="35" font-weight="700" fill="{INK}">{pct:.1f}%</text>
<text x="{cx}" y="{cy+22}" text-anchor="middle" font-family="Arial" font-size="14" fill="{MUTED}">subscribed</text>
<circle cx="600" cy="225" r="7" fill="{CORAL}"/><text x="617" y="230" font-family="Arial" font-size="17" fill="{INK}">Subscribers</text><text x="795" y="230" text-anchor="end" font-family="Arial" font-size="17" font-weight="700" fill="{INK}">{yes:,}</text>
<circle cx="600" cy="285" r="7" fill="{PALE}"/><text x="617" y="290" font-family="Arial" font-size="17" fill="{INK}">Non-subscribers</text><text x="795" y="290" text-anchor="end" font-family="Arial" font-size="17" font-weight="700" fill="{INK}">{no:,}</text>
<text x="600" y="352" font-family="Arial" font-size="14" fill="{MUTED}">Takeaway: subscribers do not spend more on average.</text>'''
    (OUT / "subscription_mix.svg").write_text(svg("Subscription mix", "Customers grouped by subscription status", body), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/customer.csv")
    parser.add_argument("--output", default="charts")
    args = parser.parse_args()
    global OUT
    OUT = Path(args.output); OUT.mkdir(parents=True, exist_ok=True)
    with Path(args.input).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    revenue = lambda key: sorted(((name, sum(float(r["purchase_amt"]) for r in rows if r[key] == name)) for name in {r[key] for r in rows}), key=lambda x: -x[1])
    counts = lambda key: sorted(((name, sum(r[key] == name for r in rows)) for name in {r[key] for r in rows}), key=lambda x: -x[1])
    bars("Revenue by gender", "Total purchase amount by customer gender", revenue("gender"), "revenue_by_gender.svg", "$", TEAL)
    bars("Revenue by category", "Total purchase amount by product category", revenue("category"), "revenue_by_category.svg", "$", TEAL)
    age = [(label.replace("_", " ").title(), value) for label, value in revenue("age_group")]
    bars("Revenue by age group", "Total purchase amount by derived age segment", age, "revenue_by_age_group.svg", "$", TEAL)
    sub = dict(counts("subscription_status")); donut(sub["Yes"], sub["No"])
    discount = defaultdict(lambda: [0, 0])
    for r in rows:
        discount[r["item_purchased"]][1] += 1
        discount[r["item_purchased"]][0] += r["discount_applied"] == "Yes"
    top_discount = sorted(((item, 100 * used / total) for item, (used, total) in discount.items()), key=lambda x: -x[1])[:5]
    bars("Highest discount-purchase rates", "Share of purchases with a discount, by product", top_discount, "discount_rate_by_product.svg", "%", GOLD)
    shipping = []
    for kind in ["Express", "Standard"]:
        values = [float(r["purchase_amt"]) for r in rows if r["shipping_type"] == kind]
        shipping.append((kind, sum(values) / len(values)))
    bars("Average spend by shipping type", "Comparison requested in Q4", shipping, "shipping_average_spend.svg", "$", CORAL)
    print(f"Created {len(list(OUT.glob('*.svg')))} charts in {OUT}")


if __name__ == "__main__":
    main()
