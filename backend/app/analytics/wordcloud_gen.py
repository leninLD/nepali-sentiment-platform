import io
import re
import unicodedata
from collections import Counter

from PIL import ImageFont
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Matches a token that is ENTIRELY Devanagari (letters, vowel signs, virama,
# nukta, digits in the Devanagari block). Anything with a Latin letter,
# ASCII digit, #, @, or stray punctuation attached fails this and gets
# dropped — this is what actually removes hashtags, mentions, and English
# words from the word cloud, independent of whatever cleaning the model's
# preprocess.py does (that pipeline intentionally keeps Latin script, since
# it's a legitimate sentiment signal for the classifier — it is NOT
# appropriate for a "Nepali word cloud").
_DEVANAGARI_TOKEN_RE = re.compile(r'^[\u0900-\u097F]+$')

# ── Confirm Pillow has complex-script shaping (Raqm/HarfBuzz) available ──────
# Without this, Devanagari conjuncts and matras can render as separated
# glyphs instead of properly joined clusters — this is the main cause of
# "words getting cut/split" for Devanagari, independent of anything below.
# If this prints False, install a Raqm-enabled Pillow build
# (system dependency: libraqm; then `pip install --upgrade --force-reinstall Pillow`).
RAQM_AVAILABLE = "raqm" in ImageFont.core.__dict__ if hasattr(ImageFont, "core") else False


def load_nepali_stopwords(path: str = "app/analytics/stop_words_nepali.txt") -> set:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {unicodedata.normalize("NFC", line.strip()) for line in f if line.strip()}
    except FileNotFoundError:
        return set()
    except Exception:
        return set()


NEPALI_STOPWORDS = load_nepali_stopwords()
FONT_PATH = "app/static/fonts/NotoSansDevanagari-VariableFont.ttf"

# Per-sentiment palettes (hex) instead of a generic matplotlib colormap —
# gives consistent, branded colors per class rather than whatever colormap
# happens to assign, and reads better against a white or transparent bg.
SENTIMENT_PALETTES = {
    "positive": ["#166534", "#15803d", "#16a34a", "#22c55e"],
    "neutral":  ["#1f2937", "#374151", "#4b5563", "#6b7280"],
    "negative": ["#991b1b", "#b91c1c", "#dc2626", "#ef4444"],
    "all":      ["#1e3a8a", "#1e40af", "#1d4ed8", "#3b82f6"],
}


def _make_color_func(palette: list[str]):
    """Cycles a fixed hex palette instead of a matplotlib colormap, so word
    cloud colors match the app's sentiment color coding exactly."""
    import random

    def color_func(word=None, font_size=None, position=None, orientation=None,
                    font_path=None, random_state=None):
        return random.choice(palette)

    return color_func


def _blank_image(message: str) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=18, color="gray")
    ax.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
    buf.seek(0)
    plt.close(fig)
    return buf


def generate_wordcloud(texts: list[str], sentiment: str = "all") -> io.BytesIO:
    """
    Generates a WordCloud image from a list of already-cleaned strings,
    removing stopwords, and returns a BytesIO buffer containing PNG data.

    `sentiment` selects a color palette: "positive" | "neutral" | "negative" | "all".
    """
    if not texts:
        return _blank_image("No words found")

    # Normalize BEFORE splitting/counting, not just after filtering — two
    # visually-identical Nepali strings can differ in Unicode byte sequence
    # (decomposed vs. composed forms), which otherwise silently splits one
    # word's count across two dict entries.
    words = []
    for t in texts:
        normalized = unicodedata.normalize("NFC", t)
        # Strip hashtag/mention markers and any attached punctuation before
        # splitting, so "#Balen" or "'सरकस'" don't survive as tokens just
        # because part of the token matched Devanagari.
        normalized = re.sub(r'[#@]\S*', ' ', normalized)
        normalized = re.sub(r'[^\u0900-\u097F\s]', ' ', normalized)
        words.extend([w for w in normalized.split() if w])

    filtered_words = [
        w for w in words
        if _DEVANAGARI_TOKEN_RE.match(w)     # drop anything not pure Devanagari
        and w not in NEPALI_STOPWORDS
        and len(w) > 1                        # drop single leftover matras/marks
    ]

    word_counts = Counter(filtered_words)
    if not word_counts:
        return _blank_image("No valid words found")

    palette = SENTIMENT_PALETTES.get(sentiment, SENTIMENT_PALETTES["all"])

    wc = WordCloud(
        font_path=FONT_PATH,
        width=1000,
        height=500,
        scale=2,                 # supersample, then downscale — sharper conjuncts
        background_color=None,
        mode="RGBA",
        color_func=_make_color_func(palette),
        max_words=50,            # fewer words = less crowding/overlap
        prefer_horizontal=1.0,   # no rotation — rotated Devanagari is where
                                 # clipping/splitting shows up worst, since
                                 # WordCloud's rotation math assumes Latin
                                 # glyph metrics
        relative_scaling=0.55,   # narrower size gap between biggest and
                                 # smallest word — one huge outlier word
                                 # (like "#balen" in the messy example)
                                 # visually dominated and crowded everything
                                 # else into illegibly small text
        min_font_size=14,        # small conjuncts need a floor size or the
                                 # matra/virama marks become illegible
        max_font_size=120,
        margin=10,
        collocations=False,
    ).generate_from_frequencies(word_counts)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0,
                transparent=True, dpi=150)
    buf.seek(0)
    plt.close(fig)

    return buf