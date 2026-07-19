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


def _normalise(text: str) -> str:
    text = text.lower()
    # collapse to unify input
    text = unicodedata.normalize("NFC", text)
    # characters not covered by unicode decomposition
    text = _map_characters(
        text, TRANSLITERATIONS
    )
    # decompose and remove combining characters
    normalised = unicodedata.normalize("NFKD", text)
    normalised = "".join(
        [char for char in normalised if not unicodedata.combining(char)]
    )
    normalised = re.sub(r"[^a-z0-9\s]", "", normalised)
    normalised = re.sub(r"\s+", "-", normalised)
    normalised = normalised.strip("-")
    return normalised


def generate_slug(title: str) -> str:
    slug = _normalise(title)
    return slug if slug else "fallback-recipe-slug"


def add_suffix(slug: str, suffix: int) -> str:
    return f"{slug}-{suffix}"
