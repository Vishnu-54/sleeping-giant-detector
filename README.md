# Sleeping Giant Detector

Find Amazon products with strong demand but weak listings, then generate AI rewrites, outreach emails, PDF reports, and client pitch decks.

## Features

- Scrape Amazon India search results via ScraperAPI
- Enrich listings with bullets, descriptions, BSR, images, brand, and A+ content signals
- Score listing quality with Claude across title, bullets, description, visuals, and social proof
- Estimate monthly revenue from BSR and price
- Rank "Sleeping Giants" by revenue opportunity
- Generate optimized listings, cold emails, PDF reports, and 5-slide `.pptx` pitch decks

## Setup

```bash
pip install -r requirements.txt
copy .env.example .env
```

Fill in `.env`:

```env
SCRAPER_API_KEY=your_scraperapi_key
GEMINI_API_KEY=your_gemini_key
LLM_PROVIDER=local
GEMINI_MODEL=gemini-2.5-flash
```

Run locally:

```bash
streamlit run app.py
```

## Streamlit Cloud Secrets

Use this in Advanced settings:

```toml
SCRAPER_API_KEY = "your_key_here"
LLM_PROVIDER = "local"
GEMINI_MODEL = "gemini-2.5-flash"
```
