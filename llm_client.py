# llm_client.py
# Small model-provider wrapper. Defaults to Gemini because it has an official free tier.

from dotenv import load_dotenv

from utils import get_secret

load_dotenv()


def generate_text(prompt, max_tokens=800):
    """Generate text with Gemini by default, with Anthropic kept as an optional fallback."""
    provider = str(get_secret("LLM_PROVIDER", "gemini")).lower()

    if provider == "local":
        raise RuntimeError("LLM_PROVIDER=local, using deterministic demo fallbacks.")

    if provider == "anthropic":
        return _generate_with_anthropic(prompt, max_tokens)

    return _generate_with_gemini(prompt, max_tokens)


def _generate_with_gemini(prompt, max_tokens):
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY. Create one free at Google AI Studio.")

    from google import genai
    from google.genai import types

    model = get_secret("GEMINI_MODEL", "gemini-2.5-flash")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=max_tokens),
    )
    return response.text or ""


def _generate_with_anthropic(prompt, max_tokens):
    api_key = get_secret("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ANTHROPIC_API_KEY. Add it to .env or Streamlit secrets.")

    import anthropic

    model = get_secret("ANTHROPIC_MODEL", "claude-haiku-4-5")
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
