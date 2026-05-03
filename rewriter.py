# rewriter.py
# Rewrites listings and generates cold outreach emails.

from dotenv import load_dotenv

from local_fallbacks import fallback_email, fallback_rewrite
from llm_client import generate_text

load_dotenv()


def rewrite_listing(product_data, weaknesses):
    """Generate optimized version of a weak listing."""
    weaknesses_text = "\n".join([f"- {w}" for w in weaknesses])
    bullets_text = "\n".join([f"- {b}" for b in product_data.get("bullets", [])])

    prompt = f"""
You are the world's best Amazon conversion copywriter.

ORIGINAL LISTING THAT NEEDS FIXING:
Product Title: {product_data.get('title')}
Current Bullets:
{bullets_text}
Current Description: {product_data.get('description', 'None')}

KNOWN WEAKNESSES TO FIX:
{weaknesses_text}

REWRITE RULES:
Title:
- Max 200 characters
- Format: [Brand] [Main Keyword] [Key Benefit] [Secondary Feature]
- No caps lock spam

Bullets, write exactly 5:
- Each starts with 2-3 WORD BOLD BENEFIT IN CAPS ->
- Then explain HOW the feature delivers that benefit
- Include one sensory or emotional word per bullet
- End one bullet with a trust signal

Description:
- Open with the customer's pain point
- 3-4 sentences max
- End with a soft CTA

RESPOND IN EXACTLY THIS FORMAT, with no extra text:

TITLE:
[new title]

BULLETS:
- [bullet 1]
- [bullet 2]
- [bullet 3]
- [bullet 4]
- [bullet 5]

DESCRIPTION:
[new description]

UPLIFT NOTE:
[One sentence: estimated percent CVR improvement and why]
"""

    try:
        return generate_text(prompt, max_tokens=800)
    except Exception as e:
        if "LLM_PROVIDER=local" not in str(e):
            print(f"Rewrite failed, using local fallback: {e}")
        return fallback_rewrite(product_data, weaknesses)


def generate_cold_email(product_data):
    """Generate personalized cold email to the listing owner."""
    weakness = product_data.get("weaknesses", ["weak listing copy"])[0]
    revenue = product_data.get("estimated_revenue", 0)
    uplift_pct = product_data.get("uplift_percent", 20)

    prompt = f"""
Write a cold email to the Amazon seller of this product.

THEIR PRODUCT: {product_data.get('title', '')[:100]}
THEIR REVIEWS: {product_data.get('review_count', 0)} reviews at {product_data.get('rating', 0)} stars
THEIR LISTING SCORE: {product_data.get('listing_score', 0)}/100
BIGGEST WEAKNESS: {weakness}
ESTIMATED MONTHLY REVENUE: Rs.{revenue:,}
POTENTIAL UPLIFT: {uplift_pct:.0f}%

RULES:
- Under 120 words total
- Subject line must reference their specific product
- First line must be hyper-specific to their product, not generic
- Mention the revenue opportunity with a real number
- One CTA only: reply to see their optimized listing
- Tone: peer-to-peer, not salesy, not formal

FORMAT:
Subject: [subject line]

[email body]
"""

    try:
        return generate_text(prompt, max_tokens=300)
    except Exception as e:
        if "LLM_PROVIDER=local" not in str(e):
            print(f"Email generation failed, using local fallback: {e}")
        return fallback_email(product_data)
