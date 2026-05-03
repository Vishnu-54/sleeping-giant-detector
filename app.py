# app.py - Main Streamlit Application

import difflib
import time

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from pdf_generator import generate_pdf
from pitch_deck import generate_pitch_deck
from revenue_estimator import calculate_revenue_uplift, estimate_revenue
from rewriter import generate_cold_email, rewrite_listing
from scorer import score_listing
from scraper import scrape_amazon_search, scrape_product_page


st.set_page_config(
    page_title="Sleeping Giant Detector",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(255, 69, 0, 0.20), transparent 28%),
        radial-gradient(circle at 90% 16%, rgba(40, 167, 69, 0.14), transparent 26%),
        linear-gradient(135deg, #101018 0%, #171720 45%, #11151c 100%);
    color: #f7f7f8;
}

[data-testid="stSidebar"] {
    background: rgba(18, 18, 28, 0.96);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stHeader"] {
    background: rgba(16, 16, 24, 0);
}

h1, h2, h3 {
    letter-spacing: 0;
}

.hero-shell {
    padding: 30px 34px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 8px;
    background:
        linear-gradient(135deg, rgba(255,69,0,0.22), rgba(40,167,69,0.08)),
        rgba(255,255,255,0.055);
    box-shadow: 0 24px 70px rgba(0,0,0,0.28);
}

.hero-kicker {
    color: #ffb199;
    font-weight: 800;
    font-size: 13px;
    text-transform: uppercase;
}

.hero-title {
    color: #ffffff;
    font-size: 52px;
    line-height: 1;
    font-weight: 900;
    margin: 8px 0 10px;
}

.hero-subtitle {
    color: #d5d7de;
    font-size: 18px;
    max-width: 820px;
}

.product-card {
    min-height: 250px;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.11);
    background: rgba(255,255,255,0.065);
    box-shadow: 0 18px 40px rgba(0,0,0,0.18);
}

.product-card img {
    width: 100%;
    height: 120px;
    object-fit: contain;
    background: #ffffff;
    border-radius: 8px;
    padding: 8px;
}

.product-name {
    color: #ffffff;
    font-weight: 800;
    font-size: 14px;
    line-height: 1.25;
    margin-top: 10px;
}

.product-meta {
    color: #cfd2dc;
    font-size: 12px;
    margin-top: 8px;
}

.stMetric {
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 8px;
    padding: 14px 16px;
}

[data-testid="stMetricLabel"] {
    color: #bfc3cf;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 900;
}

.stDataFrame {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 8px;
    overflow: hidden;
}

.streamlit-expanderHeader {
    font-weight: 800;
}

.metric-card {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    border-left: 4px solid #ff4500;
}
.giant-rank {
    font-size: 48px;
    font-weight: 900;
    color: #ff4500;
}
.score-bad { color: #dc3545; font-weight: bold; }
.score-ok  { color: #ffc107; font-weight: bold; }
.score-good{ color: #28a745; font-weight: bold; }
.stDownloadButton button, .stButton button {
    border-radius: 8px;
    font-weight: 800;
    border: 1px solid rgba(255,255,255,0.16);
}

.wow-panel {
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    background:
        linear-gradient(135deg, rgba(255, 69, 0, 0.18), rgba(0, 0, 0, 0.10)),
        rgba(255, 255, 255, 0.075);
    box-shadow: 0 24px 80px rgba(0,0,0,0.34);
    padding: 22px;
    margin: 8px 0 22px;
    overflow: hidden;
}

.wow-kicker {
    color: #ffb199;
    font-size: 12px;
    font-weight: 900;
    text-transform: uppercase;
}

.wow-title {
    color: #ffffff;
    font-size: 24px;
    line-height: 1.12;
    font-weight: 900;
    margin: 6px 0 10px;
    overflow-wrap: anywhere;
}

.wow-subtitle {
    color: #d7dae4;
    font-size: 14px;
    line-height: 1.5;
}

.wow-image {
    width: 100%;
    height: 180px;
    object-fit: contain;
    background: #ffffff;
    border-radius: 8px;
    padding: 12px;
}

.insight-strip {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 14px;
}

.insight-pill {
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.075);
    padding: 12px;
}

.insight-label {
    color: #aeb4c2;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
}

.insight-value {
    color: #ffffff;
    font-size: 18px;
    font-weight: 900;
    margin-top: 4px;
}

.asset-card {
    min-height: 132px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.07);
    padding: 15px;
}

.asset-card-title {
    color: #ffffff;
    font-weight: 900;
    font-size: 15px;
    margin-bottom: 8px;
}

.asset-card-copy {
    color: #cfd3de;
    font-size: 13px;
    line-height: 1.45;
    overflow-wrap: anywhere;
}

.clean-diff-card {
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.065);
    padding: 16px;
    min-height: 260px;
}

.clean-diff-title {
    font-size: 14px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 10px;
}

.clean-diff-list {
    margin: 0;
    padding-left: 18px;
    color: #d8dbe5;
    line-height: 1.55;
    font-size: 14px;
}

.clean-diff-list li {
    margin-bottom: 10px;
}

.before-card {
    border-left: 4px solid #dc3545;
}

.after-card {
    border-left: 4px solid #28a745;
}

@media (max-width: 760px) {
    .hero-title { font-size: 36px; }
    .insight-strip { grid-template-columns: 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
<div class="hero-shell">
  <div class="hero-kicker">Amazon opportunity intelligence</div>
  <div class="hero-title">Sleeping Giant Detector</div>
  <div class="hero-subtitle">Find products with proven demand, weak listings, and ready-to-pitch revenue upside. Scan, score, rewrite, email, deck, and report in one workflow.</div>
</div>
""",
    unsafe_allow_html=True,
)
st.divider()


with st.sidebar:
    st.header("Filters")

    num_results = st.slider(
        "Products to scan",
        min_value=5,
        max_value=30,
        value=15,
        help="More products means slower analysis but broader coverage.",
    )

    min_reviews = st.number_input(
        "Minimum reviews",
        min_value=0,
        value=0,
        help="Filter out products without enough proof of demand.",
    )

    max_score = st.slider(
        "Max listing score",
        min_value=10,
        max_value=80,
        value=55,
        help="Lower values find weaker listings.",
    )

    include_sponsored = st.toggle(
        "Include sponsored listings",
        value=True,
        help="Turn this off when you want only organic opportunities. Keep it on for demos.",
    )

    st.divider()
    st.markdown("### How It Works")
    st.markdown(
        """
1. Scrapes Amazon listings
2. Scores listing quality
3. Finds high-revenue low-score products
4. Rewrites the listing
5. Calculates revenue opportunity
6. Generates outreach assets
"""
    )

    st.divider()
    st.caption("Powered by ScraperAPI + Claude AI")


col_input, col_btn = st.columns([4, 1])
with col_input:
    keyword = st.text_input(
        "Product category to analyze",
        placeholder="e.g. posture corrector, whey protein, yoga mat, air purifier",
        label_visibility="collapsed",
    )
with col_btn:
    search_clicked = st.button("Find Giants", type="primary", use_container_width=True)

st.markdown(
    "**Quick examples:** "
    + " · ".join(
        [
            f"`{k}`"
            for k in [
                "posture corrector",
                "magnesium supplement",
                "laptop stand",
                "resistance bands",
                "air purifier",
            ]
        ]
    )
)


def _score_label(score):
    if score < 35:
        return f"🔴 {score}"
    if score < 55:
        return f"🟡 {score}"
    return f"🟢 {score}"


def _safe_filename(value, fallback="product"):
    clean = "".join(ch if ch.isalnum() or ch in (" ", "_", "-") else "" for ch in value)
    clean = clean.strip().replace(" ", "_")
    return clean[:60] or fallback


def _opportunity_score(product):
    revenue = product.get("estimated_revenue", 0)
    score = product.get("listing_score", 50)
    reviews = product.get("review_count", 0)
    money_left = product.get("money_left_on_table", 0)
    revenue_points = min(30, revenue / 7000)
    weakness_points = max(0, (85 - score) * 0.8)
    proof_points = min(15, reviews / 20)
    leak_points = min(30, money_left / 2500)
    return int(min(100, revenue_points + weakness_points + proof_points + leak_points))


def _extract_rewrite_preview(rewrite):
    lines = [line.strip("- ").strip() for line in str(rewrite).splitlines() if line.strip()]
    title = ""
    bullets = []
    for idx, line in enumerate(lines):
        if line.upper() == "TITLE:" and idx + 1 < len(lines):
            title = lines[idx + 1]
        elif ":" in line and line.split(":", 1)[0].isupper() and line.upper() not in {
            "TITLE:",
            "BULLETS:",
            "DESCRIPTION:",
            "UPLIFT NOTE:",
        }:
            bullets.append(line)
    return title, bullets[:3]


if search_clicked and keyword:
    st.session_state["giants"] = []
    st.session_state["keyword"] = keyword

    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.markdown("**Step 1/4** - Scanning Amazon search results...")
    with st.spinner("Scraping search results..."):
        products = scrape_amazon_search(keyword, num_results)

    if not products:
        st.error("No products found. Check your ScraperAPI key or try a different keyword.")
        st.stop()

    progress_bar.progress(15)
    st.info(f"Found **{len(products)}** products. Enriching each listing now.")

    status_text.markdown("**Step 2/4** - Scraping full listing details...")
    enriched = []

    for i, product in enumerate(products):
        title_preview = product.get("title", "")[:60]
        status_text.markdown(
            f"**Step 2/4** - Product {i + 1}/{len(products)}: *{title_preview}...*"
        )

        try:
            if product.get("asin"):
                details = scrape_product_page(product["asin"])
                product.update(details)

            revenue, revenue_source = estimate_revenue(product)
            product["estimated_revenue"] = revenue
            product["revenue_source"] = revenue_source
            enriched.append(product)
        except Exception as e:
            print(f"Enrichment failed for {product.get('asin')}: {e}")
            continue

        progress_bar.progress(15 + int(30 * (i + 1) / len(products)))

    status_text.markdown("**Step 3/4** - AI scoring listing quality...")
    for i, product in enumerate(enriched):
        try:
            score_data = score_listing(product)
            product["listing_score"] = score_data.get("total_score", 50)
            product["score_breakdown"] = score_data
            product["weaknesses"] = score_data.get("top_3_weaknesses", [])
            product["opportunity"] = score_data.get("opportunity_summary", "")
        except Exception as e:
            print(f"Scoring failed for {product.get('asin')}: {e}")
            product["listing_score"] = 50
            product["weaknesses"] = ["Analysis unavailable"]

        progress_bar.progress(45 + int(30 * (i + 1) / max(len(enriched), 1)))

    giants = [
        p
        for p in enriched
        if (
            p.get("review_count", 0) >= min_reviews
            and p.get("listing_score", 100) <= max_score
            and p.get("estimated_revenue", 0) > 0
            and (include_sponsored or not p.get("is_sponsored", False))
        )
    ]

    st.session_state["analyzed_products"] = enriched
    st.session_state["filter_summary"] = {
        "total": len(enriched),
        "below_min_reviews": sum(1 for p in enriched if p.get("review_count", 0) < min_reviews),
        "above_max_score": sum(1 for p in enriched if p.get("listing_score", 100) > max_score),
        "zero_revenue": sum(1 for p in enriched if p.get("estimated_revenue", 0) <= 0),
        "sponsored": sum(1 for p in enriched if p.get("is_sponsored", False)),
        "review_revenue": sum(1 for p in enriched if p.get("revenue_source") == "Reviews"),
    }

    giants.sort(
        key=lambda x: x.get("estimated_revenue", 0) / max(x.get("listing_score", 50), 1),
        reverse=True,
    )

    status_text.markdown("**Step 4/4** - Generating AI rewrites for top giants...")
    for i, giant in enumerate(giants[:5]):
        try:
            giant["rewrite"] = rewrite_listing(giant, giant.get("weaknesses", []))
            opt_rev, money_left, uplift_pct = calculate_revenue_uplift(
                giant.get("listing_score", 50),
                giant.get("estimated_revenue", 0),
            )
            giant["optimized_revenue"] = opt_rev
            giant["money_left_on_table"] = money_left
            giant["uplift_percent"] = uplift_pct
        except Exception as e:
            print(f"Rewrite failed for giant {i}: {e}")

        progress_bar.progress(75 + int(20 * (i + 1) / max(len(giants[:5]), 1)))

    progress_bar.progress(100)
    status_text.markdown("**Analysis complete.**")

    st.session_state["giants"] = giants
    time.sleep(0.5)
    status_text.empty()
    progress_bar.empty()


if "giants" in st.session_state:
    giants = st.session_state.get("giants", [])
    keyword = st.session_state.get("keyword", "")

    if not giants:
        st.warning(
            "No sleeping giants found. Try lowering minimum reviews or increasing max listing score."
        )
        summary = st.session_state.get("filter_summary", {})
        if summary:
            st.markdown("### Filter Summary")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Analyzed", summary.get("total", 0))
            c2.metric("Too Few Reviews", summary.get("below_min_reviews", 0))
            c3.metric("Score Too High", summary.get("above_max_score", 0))
            c4.metric("Sponsored", summary.get("sponsored", 0))
            st.caption(
                f"{summary.get('review_revenue', 0)} products used review-based revenue fallback because BSR was missing."
            )

        analyzed = st.session_state.get("analyzed_products", [])
        if analyzed:
            st.markdown("### Products Found")
            fallback_rows = []
            for p in analyzed:
                fallback_rows.append(
                    {
                        "Product": p.get("title", "")[:65],
                        "Reviews": p.get("review_count", 0),
                        "Score": p.get("listing_score", "N/A"),
                        "Revenue": f"₹{p.get('estimated_revenue', 0):,}/mo",
                        "Revenue Source": p.get("revenue_source", "N/A"),
                        "Sponsored": "Yes" if p.get("is_sponsored") else "No",
                    }
                )
            st.dataframe(pd.DataFrame(fallback_rows), use_container_width=True, hide_index=True)
        st.stop()

    st.success(f"Found **{len(giants)} Sleeping Giants** for *{keyword}*.")

    total_opportunity = sum(g.get("money_left_on_table", 0) for g in giants[:5])
    avg_score = sum(g.get("listing_score", 0) for g in giants) / len(giants)
    top_revenue = giants[0].get("estimated_revenue", 0) if giants else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Giants Found", len(giants))
    m2.metric("Top Revenue/mo", f"₹{top_revenue:,}")
    m3.metric("Avg Listing Score", f"{avg_score:.0f}/100")
    m4.metric("Total Opportunity", f"₹{total_opportunity:,}/mo")

    st.divider()
    top_giant = giants[0]
    top_score = _opportunity_score(top_giant)
    top_rewrite_title, top_rewrite_bullets = _extract_rewrite_preview(top_giant.get("rewrite", ""))
    if not top_rewrite_title:
        top_rewrite_title = top_giant.get("title", "Optimized listing")[:110]

    st.header("Founder Demo Moment")
    wow_left, wow_right = st.columns([1.05, 1.45])
    with wow_left:
        image = top_giant.get("image_url")
        image_html = (
            f'<img class="wow-image" src="{image}" alt="Top opportunity product">'
            if image
            else '<div class="wow-image"></div>'
        )
        st.markdown(
            f"""
<div class="wow-panel">
  <div class="wow-kicker">Best seller lead found</div>
  {image_html}
  <div class="wow-title">{top_giant.get('title', '')[:116]}</div>
  <div class="wow-subtitle">This is not just a weak listing. It is a seller lead with demand, proof, and a personalized pitch angle.</div>
  <div class="insight-strip">
    <div class="insight-pill">
      <div class="insight-label">Lead score</div>
      <div class="insight-value">{top_score}/100</div>
    </div>
    <div class="insight-pill">
      <div class="insight-label">Revenue leak</div>
      <div class="insight-value">Rs.{top_giant.get('money_left_on_table', 0):,}/mo</div>
    </div>
    <div class="insight-pill">
      <div class="insight-label">Listing score</div>
      <div class="insight-value">{top_giant.get('listing_score', 0)}/100</div>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with wow_right:
        st.markdown(
            f"""
<div class="wow-panel">
  <div class="wow-kicker">Client acquisition kit generated</div>
  <div class="wow-title">From Amazon search to sales pitch in one scan.</div>
  <div class="wow-subtitle">The product has estimated revenue, visible listing weaknesses, a rewritten offer, a cold email angle, and downloadable client collateral.</div>
</div>
""",
            unsafe_allow_html=True,
        )

        kit_cols = st.columns(3)
        with kit_cols[0]:
            st.markdown(
                f"""
<div class="asset-card">
  <div class="asset-card-title">1. Audit Hook</div>
  <div class="asset-card-copy">{top_giant.get('weaknesses', ['Listing needs clearer benefits'])[0]}</div>
</div>
""",
                unsafe_allow_html=True,
            )
        with kit_cols[1]:
            bullets_html = "<br>".join(top_rewrite_bullets[:2]) if top_rewrite_bullets else top_rewrite_title
            st.markdown(
                f"""
<div class="asset-card">
  <div class="asset-card-title">2. Rewrite Preview</div>
  <div class="asset-card-copy"><strong>{top_rewrite_title[:90]}</strong><br>{bullets_html}</div>
</div>
""",
                unsafe_allow_html=True,
            )
        with kit_cols[2]:
            st.markdown(
                f"""
<div class="asset-card">
  <div class="asset-card-title">3. Outreach Angle</div>
  <div class="asset-card-copy">Tell the seller they may be leaving <strong>Rs.{top_giant.get('money_left_on_table', 0):,}/month</strong> on the table and offer the rewritten listing as proof.</div>
</div>
""",
                unsafe_allow_html=True,
            )

        action_cols = st.columns(3)
        with action_cols[0]:
            if st.button("Generate Top Email", key="wow_email"):
                st.session_state["wow_email_text"] = generate_cold_email(top_giant)
            if st.session_state.get("wow_email_text"):
                st.download_button(
                    "Download Email",
                    st.session_state["wow_email_text"],
                    file_name=f"top_lead_email_{top_giant.get('asin', 'product')}.txt",
                    key="wow_email_download",
                )
        with action_cols[1]:
            if st.button("Generate Top Deck", key="wow_deck", type="primary"):
                pptx_bytes, slide_content = generate_pitch_deck(top_giant)
                if pptx_bytes:
                    st.session_state["wow_deck"] = pptx_bytes
            if st.session_state.get("wow_deck"):
                st.download_button(
                    "Download Deck",
                    st.session_state["wow_deck"],
                    file_name=f"founder_demo_deck_{_safe_filename(top_giant.get('title', 'product')[:30])}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key="wow_deck_download",
                )
        with action_cols[2]:
            st.link_button("Open Amazon Lead", top_giant.get("url", f"https://www.amazon.in/dp/{top_giant.get('asin', '')}"))

        bridge = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=["absolute", "relative", "total"],
                x=["Current Revenue", "Monthly Leak", "Optimized Potential"],
                y=[
                    top_giant.get("estimated_revenue", 0),
                    top_giant.get("money_left_on_table", 0),
                    top_giant.get("optimized_revenue", 0),
                ],
                text=[
                    f"Rs.{top_giant.get('estimated_revenue', 0):,}",
                    f"+Rs.{top_giant.get('money_left_on_table', 0):,}",
                    f"Rs.{top_giant.get('optimized_revenue', 0):,}",
                ],
                textposition="outside",
                connector={"line": {"color": "rgba(255,255,255,0.35)"}},
                increasing={"marker": {"color": "#28a745"}},
                totals={"marker": {"color": "#ff4500"}},
            )
        )
        bridge.update_layout(
            title="The Money Story",
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#f7f7f8"},
            margin=dict(t=45, l=10, r=10, b=10),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(bridge, use_container_width=True)

    st.divider()
    st.header("Opportunity Gallery")
    gallery_cols = st.columns(min(3, len(giants)))
    for idx, giant in enumerate(giants[:3]):
        with gallery_cols[idx % len(gallery_cols)]:
            image = giant.get("image_url")
            image_html = (
                f'<img src="{image}" alt="Product image">'
                if image
                else '<div style="height:120px;background:#fff;border-radius:8px;"></div>'
            )
            st.markdown(
                f"""
<div class="product-card">
  {image_html}
  <div class="product-name">#{idx + 1} {giant.get('title', '')[:86]}</div>
  <div class="product-meta">₹{giant.get('estimated_revenue', 0):,}/mo · Score {giant.get('listing_score', 0)}/100 · {giant.get('review_count', 0):,} reviews</div>
</div>
""",
                unsafe_allow_html=True,
            )

    st.divider()
    st.header("Ranked Sleeping Giants")

    table_data = []
    for i, giant in enumerate(giants[:10]):
        score = giant.get("listing_score", 0)
        title = giant.get("title", "")
        table_data.append(
            {
                "#": i + 1,
                "Product": title[:65] + ("..." if len(title) > 65 else ""),
                "Est. Revenue": f"₹{giant.get('estimated_revenue', 0):,}/mo",
                "Revenue Source": giant.get("revenue_source", "N/A"),
                "Reviews": f"⭐ {giant.get('rating', 0)} ({giant.get('review_count', 0):,})",
                "Listing Score": f"{_score_label(score)}/100",
                "Opportunity": giant.get("opportunity", "")[:70],
            }
        )

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.header("Deep Dive Analysis")

    for i, giant in enumerate(giants[:5]):
        score = giant.get("listing_score", 0)
        revenue = giant.get("estimated_revenue", 0)
        money_left = giant.get("money_left_on_table", 0)
        title = giant.get("title", "")

        with st.expander(
            f"#{i + 1} - {title[:75]}... | Score: {score}/100 | ₹{revenue:,}/mo",
            expanded=(i == 0),
        ):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Est. Revenue", f"₹{revenue:,}/mo")
            c2.metric(
                "Listing Score",
                f"{score}/100",
                delta="Poor" if score < 35 else "Fair" if score < 55 else "OK",
                delta_color="inverse",
            )
            c3.metric(
                "Rating",
                f"{giant.get('rating', 0)} ({giant.get('review_count', 0):,})",
            )
            if money_left:
                c4.metric(
                    "Revenue Gap",
                    f"₹{money_left:,}/mo",
                    delta=f"+{giant.get('uplift_percent', 0):.0f}% potential",
                    delta_color="normal",
                )

            if giant.get("image_url"):
                img_col, info_col = st.columns([1, 2])
                with img_col:
                    st.image(giant["image_url"], caption="Product image", use_column_width=True)
                with info_col:
                    st.markdown("#### Product Snapshot")
                    st.markdown(f"**Brand:** {giant.get('brand', 'Unknown')}")
                    st.markdown(f"**Price:** {giant.get('price', 'N/A')}")
                    st.markdown(f"**Revenue source:** {giant.get('revenue_source', 'N/A')}")
                    st.markdown(f"**Images found:** {giant.get('image_count', 0)}")

            breakdown = giant.get("score_breakdown", {})
            if breakdown:
                categories = ["Title", "Bullets", "Description", "Visuals", "Social Proof"]
                scores_vals = [
                    breakdown.get("title_score", 0),
                    breakdown.get("bullets_score", 0),
                    breakdown.get("description_score", 0),
                    breakdown.get("visual_score", 0),
                    breakdown.get("social_score", 0),
                ]

                fig = go.Figure(
                    go.Bar(
                        x=categories,
                        y=scores_vals,
                        marker_color=[
                            "#dc3545" if v < 8 else "#ffc107" if v < 14 else "#28a745"
                            for v in scores_vals
                        ],
                        text=[f"{v}/20" for v in scores_vals],
                        textposition="outside",
                    )
                )
                fig.update_layout(
                    title="Listing Quality Breakdown",
                    yaxis_range=[0, 22],
                    height=280,
                    margin=dict(t=40, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("What's Killing This Listing")
            for weakness in giant.get("weaknesses", []):
                st.error(f"- {weakness}")

            st.divider()
            st.subheader("AI-Powered Listing Rewrite")

            col_before, col_after = st.columns(2)

            with col_before:
                st.markdown("#### Original")
                st.markdown("**Title:**")
                st.info(giant.get("title", "N/A"))
                st.markdown("**Bullet Points:**")
                bullets = giant.get("bullets", [])
                if bullets:
                    for bullet in bullets:
                        st.markdown(f"- {bullet}")
                else:
                    st.caption("No bullets found")
                st.markdown("**Description:**")
                st.caption(giant.get("description", "No description found")[:300])

            with col_after:
                st.markdown("#### Rewritten")
                rewrite = giant.get("rewrite", "")
                if rewrite:
                    st.success(rewrite)
                else:
                    st.caption("Rewrite not available")

            if giant.get("bullets") and giant.get("rewrite"):
                st.subheader("What Changed")

                original_text = "\n".join(giant.get("bullets", []))
                rewrite_text = giant.get("rewrite", "")
                if "BULLETS:" in rewrite_text:
                    rewrite_text = rewrite_text.split("BULLETS:", 1)[1]
                    if "DESCRIPTION:" in rewrite_text:
                        rewrite_text = rewrite_text.split("DESCRIPTION:", 1)[0]

                diff = difflib.HtmlDiff(wrapcolumn=60)
                diff_html = diff.make_table(
                    original_text.splitlines(),
                    rewrite_text.splitlines(),
                    fromdesc="Original Bullets",
                    todesc="Optimized Bullets",
                    context=True,
                )

                styled_diff = f"""
                <style>
                    .diff td {{ font-size: 12px; padding: 3px 6px; }}
                    .diff_header {{ background: #e9ecef; }}
                    td.diff_add {{ background: #d4edda; }}
                    td.diff_chg {{ background: #fff3cd; }}
                    td.diff_sub {{ background: #f8d7da; }}
                </style>
                {diff_html}
                """
                components.html(styled_diff, height=350, scrolling=True)

            st.divider()
            st.subheader("1-Click Cold Email")
            st.caption("Ready-to-send outreach to the listing owner.")

            email_key = f"email_generated_{i}"
            if st.button("Generate Personalized Email", key=f"gen_email_{i}"):
                with st.spinner("Writing personalized email..."):
                    email_text = generate_cold_email(giant)
                st.session_state[email_key] = email_text

            if st.session_state.get(email_key):
                st.code(st.session_state[email_key], language=None)
                st.download_button(
                    "Download Email",
                    st.session_state[email_key],
                    file_name=f"outreach_{giant.get('asin', 'product')}.txt",
                    key=f"dl_email_{i}",
                )

            st.divider()
            st.subheader("Auto Client Pitch Deck")
            st.caption("One click creates a professional 5-slide deck for this product.")

            pitch_key = f"pitch_generated_{i}"
            if st.button("Generate Pitch Deck", key=f"gen_pitch_{i}", type="primary"):
                with st.spinner("Building your pitch deck... this can take 10-15 seconds."):
                    pptx_bytes, slide_content = generate_pitch_deck(giant)

                if pptx_bytes:
                    st.session_state[pitch_key] = {
                        "bytes": pptx_bytes,
                        "content": slide_content,
                    }
                    st.success("Pitch deck ready.")
                else:
                    st.error("Pitch deck generation failed. Try again.")

            if st.session_state.get(pitch_key):
                stored = st.session_state[pitch_key]
                content = stored.get("content", {})
                product_name = _safe_filename(giant.get("title", "product")[:30])

                st.download_button(
                    label="Download Pitch Deck (.pptx)",
                    data=stored["bytes"],
                    file_name=f"pitch_{product_name}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key=f"dl_pitch_{i}",
                )

                st.markdown("#### Preview Slide Content")
                if content.get("slide1"):
                    s1 = content["slide1"]
                    st.markdown("**Slide 1 - Product Snapshot**")
                    st.info(
                        f"""
**{s1.get('product_name')}**
_{s1.get('tagline')}_

Revenue: {s1.get('monthly_revenue')} | Score: {s1.get('listing_score')} | {s1.get('review_count')} reviews
"""
                    )

                if content.get("slide2"):
                    s2 = content["slide2"]
                    st.markdown("**Slide 2 - What's Wrong**")
                    st.error(
                        f"""
{s2.get('subtitle')}

1. {s2.get('weakness_1')}
2. {s2.get('weakness_2')}
3. {s2.get('weakness_3')}

{s2.get('closing_line')}
"""
                    )

                if content.get("slide3"):
                    s3 = content["slide3"]
                    st.markdown("**Slide 3 - Revenue Opportunity**")
                    st.warning(
                        f"""
Current: {s3.get('current_revenue')}/mo
Being lost: {s3.get('money_left')}/mo
With optimization: {s3.get('optimized_revenue')}/mo (+{s3.get('uplift_percent')})

{s3.get('insight')}
"""
                    )

                if content.get("slide4"):
                    s4 = content["slide4"]
                    st.markdown("**Slide 4 - Optimized Listing**")
                    st.success(
                        f"""
**New Title:** {s4.get('new_title')}

- {s4.get('bullet_1')}
- {s4.get('bullet_2')}
- {s4.get('bullet_3')}

{s4.get('improvement_note')}
"""
                    )

                if content.get("slide5"):
                    s5 = content["slide5"]
                    st.markdown("**Slide 5 - Why Us**")
                    st.info(
                        f"""
**{s5.get('value_prop')}**

1. {s5.get('point_1')}
2. {s5.get('point_2')}
3. {s5.get('point_3')}

**{s5.get('cta')}**
{s5.get('risk_reversal')}
"""
                    )

            if giant.get("asin"):
                st.link_button("View on Amazon", f"https://www.amazon.in/dp/{giant['asin']}")

    st.divider()
    st.header("Export Report")

    if st.button("Generate PDF Report", type="secondary"):
        with st.spinner("Generating PDF..."):
            try:
                pdf_bytes = generate_pdf(keyword, giants)
                st.download_button(
                    "Download PDF Report",
                    pdf_bytes,
                    file_name=f"sleeping_giants_{_safe_filename(keyword)}.pdf",
                    mime="application/pdf",
                )
                st.success("PDF ready.")
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

elif not search_clicked:
    st.markdown("### How To Use This Tool")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
**Step 1: Enter a category**

Type any Amazon product category like "yoga mat" or "protein powder".
"""
        )
    with col2:
        st.markdown(
            """
**Step 2: We scan Amazon**

Analyze listings and score each one on 5 quality dimensions.
"""
        )
    with col3:
        st.markdown(
            """
**Step 3: Find the giants**

Get ranked opportunities with rewrites, emails, reports, and pitch decks.
"""
        )


st.markdown("---")
st.caption("Built for Pixii.ai Founding Engineer Challenge | ScraperAPI + AI-assisted copy + Streamlit")
