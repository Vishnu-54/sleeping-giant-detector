# utils.py - Helper functions used across all modules

import os
import re


def get_secret(name, default=None):
    """Read a secret from environment variables or Streamlit Cloud secrets."""
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        return st.secrets.get(name, default)
    except Exception:
        return default


def clean_price(price_str):
    """Convert 'Rs.1,299' or '₹1,299' to 1299.0."""
    if not price_str:
        return 0
    try:
        text = str(price_str).replace(",", "")
        text = re.sub(r"(?i)\brs\.?\s*", "", text)
        text = text.replace("₹", "").strip()
        match = re.search(r"\d+(?:\.\d+)?", text)
        return float(match.group(0)) if match else 0
    except Exception:
        return 0


def clean_number(num_str):
    """Convert '2,341 ratings' to 2341."""
    if not num_str:
        return 0
    try:
        cleaned = re.sub(r"[^\d]", "", str(num_str))
        return int(cleaned) if cleaned else 0
    except Exception:
        return 0


def truncate(text, length=100):
    """Truncate text for display."""
    if not text:
        return "N/A"
    return text[:length] + "..." if len(text) > length else text


def safe_get(dictionary, key, default="N/A"):
    """Safe dictionary access."""
    return dictionary.get(key) or default
