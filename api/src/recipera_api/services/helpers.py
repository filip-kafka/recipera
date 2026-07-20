import re
import unicodedata

TRANSLITERATIONS = {
    "ø": "o",
    "æ": "ae",
    "þ": "th",
    "ð": "d",
    "đ": "d",
    "ŧ": "t",
    "ß": "ss",
}


def _map_characters(text: str, mapping: dict) -> str:
    return text.translate(str.maketrans(mapping))


def _normalize_slug(text: str) -> str:
    text = text.lower()
    # collapse to unify input
    text = unicodedata.normalize("NFC", text)
    # characters not covered by unicode decomposition
    text = _map_characters(text, TRANSLITERATIONS)
    # decompose and remove combining characters
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(
        [char for char in normalized if not unicodedata.combining(char)]
    )
    normalized = re.sub(r"[^a-z0-9\s]", "", normalized)
    normalized = re.sub(r"\s+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized


def generate_slug(title: str) -> str:
    slug = _normalize_slug(title)
    return slug if slug else "fallback-recipe-slug"


def add_suffix(slug: str, suffix: int) -> str:
    return f"{slug}-{suffix}"


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.lower().strip())
