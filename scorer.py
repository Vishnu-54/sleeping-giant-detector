# scorer.py
# Uses Claude to score listing quality on 5 dimensions.

import json

from dotenv import load_dotenv

from local_fallbacks import heuristic_score_listing
from llm_client import generate_text

load_dotenv()

SCORE_PROMPT = """
You are an Amazon listing optimization expert with 10+ years experience.

Score this listing and identify exact weaknesses.

=== LISTING DATA ===
Title: {title}
Brand: {brand}
Price: {price}
Rating: {rating} stars ({review_count} reviews)
Images: {image_count} images
Has A+ Content: {has_aplus}

Bullet Points:
{bullets}

Description:
{description}

=== SCORING CRITERIA ===
Score each category 0-20:

1. TITLE (0-20)
   - 20: Has main keyword, benefit, and brand. 150-200 chars. Readable.
   - 10: Has keywords but missing benefits or too short
   - 0: Generic, vague, no keywords

2. BULLETS (0-20)
   - 20: Each starts with BOLD BENEFIT, explains feature, emotional language
   - 10: Features listed but no emotional hook
   - 0: Plain features, no formatting, no benefits

3. DESCRIPTION (0-20)
   - 20: Story-driven, addresses pain points, has CTA
   - 10: Informational but boring
   - 0: Missing or copy-paste from bullets

4. VISUALS (0-20)
   - 20: 7+ images + A+ content
   - 10: 4-6 images, no A+ content
   - 0: 1-3 images, no A+ content

5. SOCIAL PROOF (0-20)
   - 20: Reviews mentioned in bullets, specific numbers used
   - 10: Good ratings but not leveraged in copy
   - 0: Zero mention of reviews/trust signals

=== RESPOND ONLY IN THIS JSON FORMAT ===
{{
  "total_score": <number 0-100>,
  "title_score": <number 0-20>,
  "bullets_score": <number 0-20>,
  "description_score": <number 0-20>,
  "visual_score": <number 0-20>,
  "social_score": <number 0-20>,
  "top_3_weaknesses": [
    "Specific weakness 1 with exact detail",
    "Specific weakness 2 with exact detail",
    "Specific weakness 3 with exact detail"
  ],
  "opportunity_summary": "One sentence describing the single biggest opportunity"
}}
"""


def _extract_json(raw):
    raw = raw.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def score_listing(product_data):
    """Score a single listing using Claude."""
    bullets_text = "\n".join([f"- {b}" for b in product_data.get("bullets", [])])
    if not bullets_text:
        bullets_text = "NO BULLETS FOUND"

    prompt = SCORE_PROMPT.format(
        title=product_data.get("title", "N/A"),
        brand=product_data.get("brand", "Unknown"),
        price=product_data.get("price", "N/A"),
        rating=product_data.get("rating", 0),
        review_count=product_data.get("review_count", 0),
        image_count=product_data.get("image_count", 0),
        has_aplus=product_data.get("has_aplus", False),
        bullets=bullets_text,
        description=product_data.get("description", "NO DESCRIPTION FOUND")[:400],
    )

    try:
        raw = generate_text(prompt, max_tokens=600).strip()
        return _extract_json(raw)

    except Exception as e:
        if "LLM_PROVIDER=local" not in str(e):
            print(f"Scoring failed, using local fallback: {e}")
        return heuristic_score_listing(product_data)


if __name__ == "__main__":
    fake_product = {
        "title": "Yoga Mat Non Slip Exercise Mat",
        "brand": "Sample Brand",
        "price": "Rs.999",
        "rating": 4.3,
        "review_count": 1340,
        "image_count": 3,
        "has_aplus": False,
        "bullets": ["Non slip mat", "Good quality", "Easy to use"],
        "description": "Yoga mat for exercise.",
    }
    print(score_listing(fake_product))
