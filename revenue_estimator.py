# revenue_estimator.py
# Converts Amazon BSR + price into estimated monthly revenue.

from utils import clean_price


# BSR -> estimated monthly sales units.
BSR_SALES_MAP = [
    (50, 4000),
    (100, 3000),
    (250, 2000),
    (500, 1500),
    (1000, 800),
    (2500, 400),
    (5000, 250),
    (10000, 120),
    (25000, 60),
    (50000, 25),
    (100000, 10),
]


def estimate_monthly_sales(bsr):
    """Given BSR, return estimated monthly unit sales."""
    if not bsr or bsr <= 0:
        return 0

    for rank_threshold, sales in BSR_SALES_MAP:
        if bsr <= rank_threshold:
            return sales
    return 5


def estimate_monthly_revenue(bsr, price):
    """Return estimated monthly revenue in INR."""
    sales = estimate_monthly_sales(bsr)
    price_value = clean_price(price)

    if price_value == 0:
        price_value = 500

    return int(sales * price_value)


def estimate_monthly_revenue_from_reviews(review_count, price):
    """
    Fallback monthly revenue estimate when BSR is missing.

    This is intentionally conservative for demo/research use:
    assume lifetime reviews represent roughly 1-3% of purchases, then dampen to
    recent monthly demand. It is less precise than BSR, but much better than 0.
    """
    price_value = clean_price(price)
    if price_value == 0:
        price_value = 500

    if not review_count or review_count <= 0:
        return int(10 * price_value)

    estimated_monthly_units = max(10, min(1200, int(review_count * 0.18)))
    return int(estimated_monthly_units * price_value)


def estimate_revenue(product):
    """Estimate revenue with BSR first, then review-count fallback."""
    bsr = product.get("bsr", 0)
    price = product.get("price", "500")
    if bsr and bsr > 0:
        return estimate_monthly_revenue(bsr, price), "BSR"
    return estimate_monthly_revenue_from_reviews(product.get("review_count", 0), price), "Reviews"


def calculate_revenue_uplift(current_score, current_revenue):
    """
    Estimate potential revenue if listing quality is improved.

    Assumption: every 10-point listing improvement roughly maps to an 8% CVR lift.
    """
    if current_score >= 100:
        return current_revenue, 0, 0

    score_gap = 100 - current_score
    uplift_percent = (score_gap / 10) * 8
    uplift_percent = min(uplift_percent, 120)

    optimized_revenue = int(current_revenue * (1 + uplift_percent / 100))
    money_left_on_table = optimized_revenue - current_revenue

    return optimized_revenue, money_left_on_table, uplift_percent
