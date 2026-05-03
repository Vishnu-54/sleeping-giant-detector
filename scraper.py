# scraper.py
# Scrapes Amazon search results and product pages via ScraperAPI.

import re
import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utils import clean_number, get_secret

load_dotenv()

SCRAPER_KEY = get_secret("SCRAPER_API_KEY")
BASE_SCRAPER_URL = "http://api.scraperapi.com"


def build_scraper_url(target_url, autoparse=False):
    """Build ScraperAPI proxy URL."""
    if not SCRAPER_KEY:
        raise RuntimeError("Missing SCRAPER_API_KEY. Add it to .env or Streamlit secrets.")

    params = {
        "api_key": SCRAPER_KEY,
        "url": target_url,
    }
    if autoparse:
        params["autoparse"] = "true"

    prepared = requests.Request("GET", BASE_SCRAPER_URL, params=params).prepare()
    return prepared.url


def scrape_amazon_search(keyword, num_results=20):
    """
    Scrape Amazon search results page.
    Returns list of basic product info dicts.
    """
    search_url = f"https://www.amazon.in/s?k={quote_plus(keyword)}&ref=nb_sb_noss"
    proxy_url = build_scraper_url(search_url)

    try:
        response = requests.get(proxy_url, timeout=60)
        response.raise_for_status()
    except Exception as e:
        print(f"Search scrape failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    products = []

    result_items = soup.select('[data-component-type="s-search-result"]')

    for item in result_items[:num_results]:
        try:
            asin = item.get("data-asin", "")
            if not asin:
                continue

            title_el = item.select_one("h2 span")
            title = title_el.get_text(strip=True) if title_el else ""

            price_el = item.select_one(".a-price .a-offscreen")
            price = price_el.get_text(strip=True) if price_el else ""

            image_el = item.select_one("img.s-image")
            image_url = image_el.get("src", "") if image_el else ""

            rating_el = item.select_one(
                '.a-icon-star-small .a-icon-alt, [data-cy="reviews-block"] .a-icon-alt'
            )
            rating_text = rating_el.get_text(strip=True) if rating_el else "0"
            try:
                rating = float(rating_text.split()[0])
            except Exception:
                rating = 0

            review_el = item.select_one(
                '[data-cy="reviews-block"] .a-size-base, .a-row .a-size-base.s-underline-text'
            )
            review_count = clean_number(review_el.get_text() if review_el else "0")

            is_sponsored = bool(
                item.select_one('.puis-sponsored-label-text, [aria-label="Sponsored"]')
            )

            if title and asin:
                products.append(
                    {
                        "asin": asin,
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "review_count": review_count,
                        "bsr": 0,
                        "is_sponsored": is_sponsored,
                        "image_url": image_url,
                        "url": f"https://www.amazon.in/dp/{asin}",
                    }
                )
        except Exception:
            continue

    return products


def scrape_product_page(asin):
    """
    Scrape full product listing details.
    Returns enriched dict with bullets, description, images, and BSR.
    """
    url = f"https://www.amazon.in/dp/{asin}"
    proxy_url = build_scraper_url(url)

    try:
        response = requests.get(proxy_url, timeout=60)
        response.raise_for_status()
    except Exception as e:
        print(f"Product page scrape failed for {asin}: {e}")
        return {}

    soup = BeautifulSoup(response.text, "lxml")
    result = {}

    bullets = []
    bullet_div = soup.find("div", {"id": "feature-bullets"})
    if bullet_div:
        for li in bullet_div.find_all("li"):
            text = li.get_text(" ", strip=True)
            if text and "Make sure this fits" not in text:
                bullets.append(text)
    result["bullets"] = bullets[:5]

    description = ""
    desc_div = soup.find("div", {"id": "productDescription"})
    if desc_div:
        description = desc_div.get_text(" ", strip=True)[:600]
    result["description"] = description

    bsr = 0
    rank_text = ""
    rank_table = soup.find("th", string=lambda t: t and "Best Sellers Rank" in t)
    if rank_table:
        rank_td = rank_table.find_next_sibling("td")
        if rank_td:
            rank_text = rank_td.get_text(" ", strip=True)

    detail_bullets = soup.select("#detailBullets_feature_div li")
    for li in detail_bullets:
        text = li.get_text(" ", strip=True)
        if "Best Sellers Rank" in text:
            rank_text = text
            break

    if rank_text:
        bsr_match = re.search(r"#([\d,]+)", rank_text)
        if bsr_match:
            bsr = clean_number(bsr_match.group(1))
    result["bsr"] = bsr

    image_block = soup.find("div", {"id": "altImages"})
    image_count = len(image_block.find_all("li")) if image_block else 1
    result["image_count"] = min(image_count, 9)

    image_el = soup.select_one("#landingImage, #imgTagWrapperId img")
    if image_el:
        result["image_url"] = image_el.get("src") or image_el.get("data-old-hires") or ""

    result["has_aplus"] = bool(
        soup.find("div", {"id": "aplus"})
        or soup.find("div", {"id": "aplus3p_feature_div"})
    )

    rating_el = soup.select_one("#acrPopover .a-icon-alt, #averageCustomerReviews .a-icon-alt")
    if rating_el:
        try:
            result["rating"] = float(rating_el.get_text(strip=True).split()[0])
        except Exception:
            pass

    review_el = soup.select_one("#acrCustomerReviewText")
    if review_el:
        result["review_count"] = clean_number(review_el.get_text(strip=True))

    brand_el = soup.find("a", {"id": "bylineInfo"})
    result["brand"] = brand_el.get_text(" ", strip=True) if brand_el else "Unknown"

    price_el = (
        soup.find("span", {"id": "priceblock_ourprice"})
        or soup.find("span", {"id": "priceblock_dealprice"})
        or soup.select_one(".a-price .a-offscreen")
        or soup.find("span", {"class": "a-price-whole"})
    )
    if price_el:
        result["price"] = price_el.get_text(strip=True)

    time.sleep(0.3)
    return result


if __name__ == "__main__":
    sample = scrape_amazon_search("yoga mat", 3)
    print(sample)
    if sample:
        print(scrape_product_page(sample[0]["asin"]))
