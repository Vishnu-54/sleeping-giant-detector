# local_fallbacks.py
# Deterministic demo fallbacks when the LLM API is unavailable.

def _product_context(product):
    title = (product.get("title", "") or "").lower()
    bullets = " ".join(product.get("bullets", []) or []).lower()
    blob = f"{title} {bullets}"
    brand = product.get("brand", "Brand").replace("Visit the ", "").replace(" Store", "")
    if brand == "Unknown":
        brand = (product.get("title", "Brand").split() or ["Brand"])[0]

    if any(word in blob for word in ["air purifier", "hepa", "pm2.5", "pollutant", "cadr"]):
        return {
            "category": "air purifier",
            "brand": brand,
            "title": f"{brand} Air Purifier for Home & Office, HEPA Filtration for Cleaner Breathing and Fresher Rooms",
            "bullets": [
                "CLEANER BREATHING: HEPA filtration captures fine dust, smoke, pollen, and airborne particles for fresher indoor air.",
                "ODOR CONTROL: Activated carbon helps reduce cooking smells, pet odors, and stale room air without harsh fragrance.",
                "ROOM-READY POWER: Designed for bedrooms, home offices, and living spaces where clean air matters every day.",
                "QUIET COMFORT: Low-noise operation keeps purification running while you work, sleep, or relax.",
                "EASY DAILY USE: Simple controls and long filter life make cleaner air feel effortless.",
            ],
            "description": "Indoor air can feel heavy even when the room looks clean. This air purifier helps reduce dust, smoke, pollen, odors, and everyday pollutants with multi-stage filtration built for daily use. Place it in your bedroom, office, or living room and let it quietly refresh the air around you. Start with cleaner breathing where you spend the most time.",
            "uplift": "Estimated 25-40% CVR improvement because the rewrite leads with cleaner breathing, odor control, room coverage, and daily comfort.",
            "deck_title": "HEPA Filtration for Cleaner Rooms",
            "deck_bullets": [
                "CLEANER BREATHING: Captures fine dust, smoke, pollen, and particles for fresher air.",
                "ODOR CONTROL: Carbon filtration helps reduce pet, cooking, and stale-room smells.",
                "QUIET COMFORT: Keeps air moving in bedrooms and offices without distracting noise.",
            ],
        }

    if any(word in blob for word in ["laptop stand", "desk", "ergonomic"]):
        return {
            "category": "laptop stand",
            "brand": brand,
            "title": f"{brand} Laptop Stand for Desk, Ergonomic Height Support for Comfortable Work Setups",
            "bullets": [
                "BETTER POSTURE: Raises your screen to a more natural eye level for less neck and shoulder strain.",
                "STEADY SUPPORT: Stable construction keeps your laptop secure through typing, calls, and daily work.",
                "COOLER WORKFLOW: Open design improves airflow to help your laptop stay cooler during long sessions.",
                "DESK-FRIENDLY FIT: Compact footprint keeps your setup clean without crowding your workspace.",
                "DAILY COMFORT: Built for office, study, and work-from-home routines.",
            ],
            "description": "A flat laptop setup can turn every workday into neck strain. This stand lifts your screen into a more comfortable position while keeping your desk organized and your laptop supported. Use it for work, study, video calls, or focused sessions. Build a cleaner setup that feels better hour after hour.",
            "uplift": "Estimated 25-40% CVR improvement because the rewrite connects ergonomic benefits to everyday work pain.",
            "deck_title": "Ergonomic Desk Comfort",
            "deck_bullets": [
                "BETTER POSTURE: Raises the screen to reduce neck and shoulder strain.",
                "STEADY SUPPORT: Keeps laptops secure during daily desk work.",
                "COOLER WORKFLOW: Open design supports airflow during long sessions.",
            ],
        }

    if any(word in blob for word in ["posture", "back support", "shoulder support", "clavicle"]):
        return {
            "category": "posture corrector",
            "brand": brand,
            "title": f"{brand} Posture Corrector Belt for Back & Shoulder Support, Adjustable Brace for Daily Comfort",
            "bullets": [
                "PAIN-FREE POSTURE: Gently guides shoulders back to reduce slouching and support a confident upright stance.",
                "ALL-DAY COMFORT: Lightweight breathable fabric feels smooth under clothes at work, home, or while commuting.",
                "CUSTOM FIT: Adjustable straps help men and women find secure support without stiff, bulky pressure.",
                "BACK SUPPORT: X-cross design targets upper back, shoulders, and clavicle alignment where posture breaks down most.",
                "TRUSTED DAILY USE: Built for repeat wear with practical support that fits into normal routines.",
            ],
            "description": "Long hours at a desk can make rounded shoulders feel normal, even when your back is asking for help. This posture corrector gives gentle support where you need it most while staying slim enough for everyday wear. Use it during work, study, walking, or light activity to build better posture habits. Choose a comfortable fit and start feeling more aligned through the day.",
            "uplift": "Estimated 25-40% CVR improvement because the rewrite turns plain support features into pain relief, comfort, and trust-led buying reasons.",
            "deck_title": "Daily Posture Comfort",
            "deck_bullets": [
                "PAIN-FREE POSTURE: Guides shoulders back for a more confident stance.",
                "ALL-DAY COMFORT: Breathable support stays discreet under clothing.",
                "CUSTOM FIT: Adjustable straps help different body types get secure support.",
            ],
        }

    return {
        "category": "product",
        "brand": brand,
        "title": f"{brand} {product.get('title', 'Product')[:80]} - Clear Benefits for Everyday Use",
        "bullets": [
            "CLEAR BENEFIT: Explains the main outcome shoppers care about before listing technical details.",
            "DAILY CONFIDENCE: Shows how the product fits into real routines and solves a practical problem.",
            "SMART DESIGN: Translates features into comfort, ease, durability, or performance benefits.",
            "EASY CHOICE: Reduces hesitation with clearer use cases and stronger buying reasons.",
            "TRUSTED VALUE: Connects product proof to a more confident purchase decision.",
        ],
        "description": "Shoppers need to understand why this product is the right choice quickly. This rewrite leads with the problem, explains the most useful benefits, and makes the buying decision feel easier. It turns feature-heavy copy into a clearer story built around outcomes, trust, and everyday use.",
        "uplift": "Estimated 20-35% CVR improvement because the rewrite makes the product benefits easier to understand.",
        "deck_title": "Clearer Product Value",
        "deck_bullets": [
            "CLEAR BENEFIT: Leads with the main buyer outcome.",
            "DAILY CONFIDENCE: Shows how the product fits real use cases.",
            "EASY CHOICE: Reduces hesitation with sharper benefit copy.",
        ],
    }


def heuristic_score_listing(product):
    """Score listing quality locally so demos do not fail when an API key is invalid."""
    title = product.get("title", "") or ""
    bullets = product.get("bullets", []) or []
    description = product.get("description", "") or ""
    image_count = product.get("image_count", 0) or 0
    has_aplus = bool(product.get("has_aplus"))
    review_count = product.get("review_count", 0) or 0

    title_score = 8
    if 80 <= len(title) <= 200:
        title_score += 4
    if any(word in title.lower() for word in ["support", "comfort", "adjustable", "pain", "corrector"]):
        title_score += 4
    if "|" not in title and len(title) < 180:
        title_score += 2
    title_score = min(20, title_score)

    bullets_score = min(20, 5 + len(bullets) * 2)
    benefit_words = ["comfort", "support", "relief", "confidence", "breathable", "adjustable"]
    bullets_blob = " ".join(bullets).lower()
    bullets_score += min(5, sum(1 for word in benefit_words if word in bullets_blob))
    bullets_score = min(20, bullets_score)

    description_score = 4 if not description else min(20, 8 + min(8, len(description) // 90))
    visual_score = 5 if image_count <= 3 else 12 if image_count <= 6 else 16
    if has_aplus:
        visual_score = min(20, visual_score + 4)
    social_score = 4
    if review_count > 100:
        social_score += 5
    if review_count > 1000:
        social_score += 4
    if any(word in bullets_blob for word in ["trusted", "rated", "reviews", "customers"]):
        social_score += 5
    social_score = min(20, social_score)

    total = title_score + bullets_score + description_score + visual_score + social_score
    weaknesses = []
    if title_score < 15:
        weaknesses.append("Title is keyword-heavy but does not lead with a clear emotional benefit.")
    if bullets_score < 15:
        weaknesses.append("Bullets explain features, but the benefit hierarchy is not strong enough.")
    if description_score < 12:
        weaknesses.append("Description is missing or too thin to overcome buyer hesitation.")
    if visual_score < 14:
        weaknesses.append("Visual stack needs more conversion assets such as lifestyle, sizing, and comparison images.")
    if social_score < 14:
        weaknesses.append("Strong reviews are not being used as trust signals in the listing copy.")

    while len(weaknesses) < 3:
        weaknesses.append("Listing has demand, but the page does not make the buying decision feel obvious.")

    return {
        "total_score": int(total),
        "title_score": int(title_score),
        "bullets_score": int(bullets_score),
        "description_score": int(description_score),
        "visual_score": int(visual_score),
        "social_score": int(social_score),
        "top_3_weaknesses": weaknesses[:3],
        "opportunity_summary": "Rewrite the listing around pain relief, trust, and daily-use outcomes.",
        "analysis_source": "Local fallback",
    }


def fallback_rewrite(product, weaknesses):
    ctx = _product_context(product)
    bullets = "\n".join(f"- {bullet}" for bullet in ctx["bullets"])

    return f"""TITLE:
{ctx["title"]}

BULLETS:
{bullets}

DESCRIPTION:
{ctx["description"]}

UPLIFT NOTE:
{ctx["uplift"]}"""


def fallback_email(product):
    title = product.get("title", "your product")[:70]
    revenue = product.get("estimated_revenue", 0)
    score = product.get("listing_score", 0)
    weakness = (product.get("weaknesses") or ["the listing is not converting demand into trust"])[0]
    money_left = product.get("money_left_on_table", int(revenue * 0.25))

    return f"""Subject: Quick idea for your {title}

I noticed your {title} has real demand, but the listing is scoring only {score}/100 in our audit.

The biggest issue: {weakness}

Based on current estimated revenue, this could be leaving around Rs.{money_left:,}/month on the table.

I rewrote the title, bullets, and description into a sharper conversion-focused version.

Reply and I’ll send the before/after audit."""


def fallback_pitch_content(giant):
    ctx = _product_context(giant)
    title = giant.get("title", "Product")
    short = title[:48]
    revenue = giant.get("estimated_revenue", 0)
    money_left = giant.get("money_left_on_table", int(revenue * 0.25))
    optimized = giant.get("optimized_revenue", revenue + money_left)
    uplift = giant.get("uplift_percent", 30)
    score = giant.get("listing_score", 0)
    weaknesses = giant.get("weaknesses", [])
    while len(weaknesses) < 3:
        weaknesses.append("The listing has demand, but the conversion story is not sharp enough.")

    return {
        "slide1": {
            "title": "Product Snapshot",
            "product_name": short,
            "monthly_revenue": f"Rs.{revenue:,}/mo",
            "star_rating": f"{giant.get('rating', 0)} stars",
            "review_count": f"{giant.get('review_count', 0):,} reviews",
            "listing_score": f"{score}/100",
            "tagline": "Strong demand. Weak listing. Clear upside.",
        },
        "slide2": {
            "title": "What's Hurting Your Sales",
            "subtitle": "The product is visible, but the listing is not converting attention into confidence.",
            "weakness_1": weaknesses[0],
            "weakness_2": weaknesses[1],
            "weakness_3": weaknesses[2],
            "closing_line": "Every unclear section creates avoidable buyer hesitation.",
        },
        "slide3": {
            "title": "The Revenue Opportunity",
            "current_revenue": f"Rs.{revenue:,}",
            "optimized_revenue": f"Rs.{optimized:,}",
            "money_left": f"Rs.{money_left:,}",
            "uplift_percent": f"{uplift:.0f}%",
            "stat_1": "Benefit-led titles improve click quality by matching buyer intent faster.",
            "stat_2": "Clear bullets reduce comparison shopping and make the add-to-cart decision easier.",
            "insight": "This product already has demand; the listing needs a stronger conversion story.",
        },
        "slide4": {
            "title": "Your Optimized Listing Preview",
            "new_title_label": "New Title",
            "new_title": ctx["title"],
            "bullet_1": ctx["deck_bullets"][0],
            "bullet_2": ctx["deck_bullets"][1],
            "bullet_3": ctx["deck_bullets"][2],
            "improvement_note": f"The rewrite sells {ctx['deck_title'].lower()}, not just product specs.",
        },
        "slide5": {
            "title": "Why Work With Us",
            "value_prop": "Turn existing demand into more revenue without changing the product.",
            "point_1": "Full listing rewrite and conversion audit delivered fast.",
            "point_2": "Before-after copy, score breakdown, and priority fixes included.",
            "point_3": "Built around buyer psychology, search intent, and trust signals.",
            "cta": "Reply to get the complete audit and optimized listing.",
            "risk_reversal": "First revision included. No long contract required.",
        },
    }
