# 🔥 Sleeping Giant Detector

**Find Amazon products that already sell, but are losing money because the listing is weak.**

Sleeping Giant Detector is a lead-generation and pitch-asset engine for Amazon marketing agencies, freelance listing copywriters, seller consultants, and e-commerce growth teams.

Type a product category like `posture corrector`, `air purifier`, or `laptop stand`. The app scans Amazon listings, estimates revenue, detects weak product pages, ranks the best opportunities, and generates the assets needed to pitch that seller immediately.

---

## 💡 The Big Idea

Most Amazon tools show data.

This app shows **action**.

Instead of only saying, “this product has demand,” Sleeping Giant Detector says:

> “This seller is probably making money, their listing is weak, they may be leaving Rs.X/month on the table, and here is the email + pitch deck you can send them today.”

That is the founder-level insight: this is not just an analytics dashboard. It is a **client acquisition machine** for Amazon service providers.

---

## 👥 Who Is This For?

- Amazon marketing agencies
- Freelance Amazon listing copywriters
- E-commerce consultants
- Product listing optimization services
- Virtual assistant agencies serving Amazon sellers
- Amazon sellers who want to audit their own listings

---

## 😩 Problem

Agencies and freelancers waste hours finding good leads manually:

1. Search Amazon categories
2. Open product pages one by one
3. Guess which sellers have revenue
4. Check reviews and listing quality
5. Manually write audit notes
6. Manually create cold emails
7. Manually prepare pitch decks

This can take **3-4 hours per qualified lead**.

---

## 🚀 Solution

Sleeping Giant Detector compresses that workflow into minutes:

1. Enter a category
2. Scrape Amazon listings
3. Estimate revenue
4. Score listing quality
5. Detect “Sleeping Giants”
6. Show revenue gap
7. Generate rewritten listing
8. Generate cold email
9. Generate client pitch deck
10. Export PDF report

The user goes from **search keyword** to **client-ready pitch assets** in one workflow.

---

## 🛌 What Is A Sleeping Giant?

A Sleeping Giant is a product with:

- Real demand
- Revenue potential
- Reviews or sales signals
- Poor listing quality
- Weak title, bullets, description, visuals, or trust signals

Formula:

```text
High estimated revenue + weak listing = warm agency lead
```

Example:

```text
Product: Posture Corrector
Estimated revenue: Rs.7,48,500/month
Listing score: 45/100
Potential revenue leak: Rs.3,29,340/month
```

That number becomes the pitch.

---

## ⚡ Founder Wow Moment

The app includes a dedicated **Founder Demo Moment** panel.

It instantly shows:

- Best seller lead found
- Product image
- Lead score
- Listing score
- Monthly revenue leak
- Audit hook
- Rewrite preview
- Outreach angle
- Revenue bridge chart
- One-click email
- One-click pitch deck
- Amazon lead link

This makes the value obvious in the first few seconds after a scan.

---

## ✨ Key Features

### 🔍 1. Amazon Category Scanner

Enter any Amazon product category and scan live search results through ScraperAPI.

Examples:

```text
posture corrector
air purifier
laptop stand
resistance bands
magnesium supplement
```

### 📊 2. Ranked Opportunity Table

Products are ranked by opportunity using:

- Estimated monthly revenue
- Listing quality score
- Revenue gap
- Reviews
- Sponsored/organic status

### 🧠 3. Listing Quality Score

Each listing is scored across 5 dimensions:

| Dimension | What It Checks |
|---|---|
| Title | Keyword clarity, benefit, readability |
| Bullets | Benefit-led copy, emotional hooks, clarity |
| Description | Pain points, story, CTA |
| Visuals | Image count and A+ content signals |
| Social Proof | Reviews and trust signals used in copy |

### 💰 4. Revenue Estimator

The app estimates monthly revenue using:

- BSR when available
- Review-based fallback when BSR is missing
- Product price

It also calculates estimated revenue left on the table.

### ✍️ 5. AI Rewrite

Generates:

- Optimized title
- 5 rewritten bullets
- Improved description
- Conversion uplift note

### 🔁 6. Visual Before/After Diff

Shows what changed between the original listing and optimized version.

### 📧 7. Cold Email Generator

Creates a personalized seller outreach email using:

- Product name
- Review count
- Listing score
- Main weakness
- Revenue gap

### 🎯 8. Auto Client Pitch Deck

Generates a downloadable 5-slide `.pptx` deck:

1. Product Snapshot
2. What Is Hurting Sales
3. Revenue Opportunity
4. Optimized Listing Preview
5. Why Work With Us

### 📄 9. PDF Report Export

Exports all Sleeping Giants into a client-ready PDF report with:

- Product image
- Revenue estimate
- Listing score
- Review count
- Revenue gap
- Top weaknesses
- Amazon link

---

## 💸 Business Value

### 🧾 User Alternative

Manual research with Amazon search, spreadsheets, and copywriting.

### ⏱️ Time Saved

```text
Manual process: 3-4 hours per lead
With this tool: minutes
```

### 🤑 How Users Make Money

Agencies and freelancers can use the generated audit, email, and deck to pitch Amazon sellers.

Example service offers:

- Amazon listing audit: Rs.2,000-10,000
- Listing rewrite package: Rs.10,000-50,000
- Monthly Amazon optimization retainer: Rs.25,000-1,00,000+
- Agency SaaS lead tool: $49-99/month

### 📈 Potential Revenue Model

```text
SaaS plan: $49/month
100 users: $4,900/month
1,000 users: $49,000/month
```

Or usage-based:

```text
Rs.99 per PDF report
Rs.199 per pitch deck
Rs.999/month for unlimited scans
```

---

## 🏆 Why This Beats Existing Tools

### 🧰 vs Helium10 / Jungle Scout

Those tools show product data.

Sleeping Giant Detector shows:

- What is wrong
- How much money may be leaking
- How to fix it
- What email to send
- What deck to pitch

### 👩‍💻 vs Hiring A VA

A VA may take days to research and prepare leads.

This app does it in minutes.

### 🐢 vs Manual Research

Manual research gives you a spreadsheet.

This app gives you a client-ready sales package.

### ⭐ Unique Angle

The cold email and pitch deck generation turns analytics into immediate ROI.

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Scraping | ScraperAPI |
| Parsing | BeautifulSoup + lxml |
| Data | pandas |
| Charts | Plotly |
| PDF | fpdf2 |
| Pitch Deck | python-pptx |
| Environment | python-dotenv |
| AI Mode | Local deterministic fallback for demo reliability |
| Optional AI | Gemini / OpenRouter / Groq-compatible future integration |

---

## 🧯 Why Local AI Fallback?

Free AI APIs often have strict rate limits.

During demos, quota crashes look bad.

So this project uses:

```env
LLM_PROVIDER=local
```

This keeps the demo reliable while still producing:

- Listing scores
- Weaknesses
- Rewrites
- Emails
- Pitch decks

The system is structured so a production version can swap in Gemini, Groq, OpenRouter, Claude, or another LLM provider.

---

## 📁 Project Structure

```text
sleeping-giant-detector/
├── app.py
├── scraper.py
├── scorer.py
├── rewriter.py
├── revenue_estimator.py
├── pdf_generator.py
├── pitch_deck.py
├── local_fallbacks.py
├── llm_client.py
├── utils.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Vishnu-54/sleeping-giant-detector.git
cd sleeping-giant-detector
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create Environment File

Copy:

```bash
copy .env.example .env
```

Fill in:

```env
SCRAPER_API_KEY=your_scraperapi_key
LLM_PROVIDER=local
GEMINI_MODEL=gemini-2.5-flash
```

### 4️⃣ Run App

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## ☁️ Streamlit Cloud Deployment

Deploy using Streamlit Community Cloud:

```text
https://share.streamlit.io
```

Use:

```text
Repository: Vishnu-54/sleeping-giant-detector
Branch: main
Main file path: app.py
```

Advanced settings secrets:

```toml
SCRAPER_API_KEY = "your_scraperapi_key"
LLM_PROVIDER = "local"
GEMINI_MODEL = "gemini-2.5-flash"
```

---

## 🎬 Best Demo Settings

Use:

```text
Keyword: posture corrector
Products to scan: 5 or 10
Minimum reviews: 0
Max listing score: 80
Include sponsored listings: ON
```

---

## 🔐 Important Security Note

Never commit `.env`.

Rotate API keys if they were exposed during testing or screenshots.

---

## 🗣️ One-Line Pitch

**Sleeping Giant Detector helps Amazon agencies find warm seller leads and generate a personalized audit, email, pitch deck, and PDF report in minutes.**
