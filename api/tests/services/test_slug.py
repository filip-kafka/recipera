import unicodedata
from recipera_api.services.slug import add_suffix, generate_slug


def test_transliteration():
    assert generate_slug("ø") == "o"
    assert generate_slug("æ") == "ae"
    assert generate_slug("þ") == "th"
    assert generate_slug("ð") == "d"
    assert generate_slug("đ") == "d"
    assert generate_slug("ŧ") == "t"
    assert generate_slug("ß") == "ss"
    assert generate_slug("testøtest") == "testotest"
    assert generate_slug("testætest") == "testaetest"
    assert generate_slug("testþtest") == "testthtest"
    assert generate_slug("testðtest") == "testdtest"
    assert generate_slug("testđtest") == "testdtest"
    assert generate_slug("testŧtest") == "testttest"
    assert generate_slug("testßtest") == "testsstest"


def test_slug_is_lowercase():
    assert generate_slug("ABCDE") == "abcde"
    assert generate_slug("abcde") == "abcde"


def test_normalisation():
    # --- NFKD-decomposable diacritics: stripped to base letter ---
    assert not any(unicodedata.combining(c) for c in generate_slug("Café"))
    assert generate_slug("Café") == "cafe"
    assert generate_slug("naïve") == "naive"
    assert generate_slug("jalapeño") == "jalapeno"
    assert generate_slug("crème brûlée") == "creme-brulee"
    assert generate_slug("G'nocchi Sauté") == "gnocchi-saute"

    # --- precomposed vs decomposed ---
    assert generate_slug("\u00e5") == generate_slug("a\u030a")
    assert generate_slug("Sm\u00f8rgasbord") == generate_slug("Smørgasbord")
    assert generate_slug("café") == generate_slug("cafe\u0301")

    # --- combining marks fully removed ---
    assert "\u0301" not in generate_slug("é")
    assert "\u030a" not in generate_slug("å")
    assert generate_slug("é").isascii()

    # --- mixed / real-world titles ---
    assert generate_slug("Køld Skål med Æbler") == "kold-skal-med-aebler"
    assert generate_slug("Crêpes Suzette (flambé)") == "crepes-suzette-flambe"
    assert (
        generate_slug("české řízečky jako od dědečka")
        == "ceske-rizecky-jako-od-dedecka"
    )

    # --- edge cases around the normalization step ---
    assert generate_slug("ÅÄÖ") == "aao"
    assert generate_slug("Æøå") == "aeoa"


def test_fallback_slug():
    assert generate_slug("") == "fallback-recipe-slug"
    assert generate_slug(" ") == "fallback-recipe-slug"
    assert generate_slug("🎂") == "fallback-recipe-slug"
    assert generate_slug("寿司") == "fallback-recipe-slug"


def test_add_suffix():
    assert add_suffix("test", 0) == "test-0"
    assert add_suffix("test", 999) == "test-999"
