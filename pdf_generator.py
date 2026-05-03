# pdf_generator.py
# Generates downloadable PDF report of all sleeping giants.

from datetime import datetime
from io import BytesIO

import requests
from fpdf import FPDF


class SleepingGiantReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(255, 69, 0)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "  SLEEPING GIANT DETECTOR", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(
            0,
            10,
            f'Page {self.page_no()} | Generated {datetime.now().strftime("%Y-%m-%d")}',
            align="C",
        )


def _safe_pdf_text(text):
    """Keep text friendly to core PDF fonts."""
    return str(text).replace("₹", "Rs.").replace("—", "-").replace("•", "-")


def _add_product_image(pdf, image_url):
    """Add a product image from URL when available."""
    if not image_url:
        return
    try:
        response = requests.get(image_url, timeout=12)
        response.raise_for_status()
        image = BytesIO(response.content)
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.image(image, x=x, y=y, w=28)
        pdf.set_xy(x + 32, y)
    except Exception:
        return


def generate_pdf(keyword, giants):
    """Generate PDF report and return bytes."""
    pdf = SleepingGiantReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 10, _safe_pdf_text(f'Sleeping Giants: "{keyword}"'), ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(
        0,
        8,
        f'Found {len(giants)} opportunities | {datetime.now().strftime("%B %d, %Y")}',
        ln=True,
    )
    pdf.ln(5)

    for i, g in enumerate(giants[:10]):
        pdf.set_fill_color(245, 245, 245)
        pdf.set_font("Helvetica", "B", 12)
        title = g.get("title", "Unknown")
        title_short = title[:70] + ("..." if len(title) > 70 else "")
        pdf.multi_cell(0, 8, _safe_pdf_text(f"#{i + 1} - {title_short}"), fill=True)

        image_y = pdf.get_y()
        _add_product_image(pdf, g.get("image_url"))

        pdf.set_font("Helvetica", "", 10)
        pdf.cell(65, 7, f"Est. Revenue: Rs.{g.get('estimated_revenue', 0):,}/mo")
        pdf.cell(65, 7, f"Listing Score: {g.get('listing_score', 0)}/100")
        pdf.cell(
            0,
            7,
            f"Reviews: {g.get('review_count', 'N/A')} ({g.get('rating', 0)} stars)",
            ln=True,
        )

        money_left = g.get("money_left_on_table", 0)
        if money_left:
            pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 7, f"Money left on table: Rs.{money_left:,}/mo", ln=True)
            pdf.set_text_color(0, 0, 0)

        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 7, "Top Weaknesses:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for weakness in g.get("weaknesses", []):
            pdf.cell(0, 6, _safe_pdf_text(f"  x {weakness[:100]}"), ln=True)

        pdf.set_font("Helvetica", "U", 9)
        pdf.set_text_color(0, 0, 200)
        pdf.cell(0, 7, f"  amazon.in/dp/{g.get('asin', '')}", ln=True)
        pdf.set_text_color(0, 0, 0)

        if g.get("image_url"):
            pdf.set_y(max(pdf.get_y(), image_y + 30))
        pdf.ln(4)

    output = pdf.output(dest="S")
    if isinstance(output, bytearray):
        return bytes(output)
    if isinstance(output, str):
        return output.encode("latin-1")
    return bytes(output)
