from recipera_api.services.helpers import normalize_name


def test_normalize_name():
    # internal whitespace is collapsed
    assert normalize_name("olive   oil") == "olive oil"
    assert normalize_name("olive\toil") == "olive oil"
    # name is lowercased
    assert normalize_name("OLIVE OIL") == "olive oil"
    # accents and non alphanumerics are not removed
    assert normalize_name("Salt & Pepper") == "salt & pepper"
    assert normalize_name("crème fraîche") == "crème fraîche"
    # all whitespace types are stripped
    assert normalize_name("\tflour\n") == "flour"
    assert normalize_name("      ") == ""
    assert normalize_name("  All-purpose Flour  ") == "all-purpose flour"
