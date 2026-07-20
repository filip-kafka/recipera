from recipera_api.db.models import Ingredient, Tag
from recipera_api.services.catalogue import create_or_get
from sqlalchemy import select


def test_create_or_get_creates_new_ingredient(session):
    ingredient = create_or_get(session, Ingredient, "test ingredient")

    assert ingredient.id is not None
    assert ingredient.name == "test ingredient"


def test_create_or_get_returns_existing_ingredient(session):
    ingredient = create_or_get(session, Ingredient, "test ingredient")
    ingredient_2 = create_or_get(session, Ingredient, "test ingredient")
    ingredient_3 = create_or_get(session, Ingredient, "  TEST    INGREDIENT   ")

    assert len(session.scalars(select(Ingredient)).all()) == 1
    assert ingredient.id == ingredient_2.id
    assert ingredient.id == ingredient_3.id
    assert ingredient.name == ingredient_2.name
    assert ingredient.name == ingredient_3.name


def test_create_or_get_creates_new_tag(session):
    tag = create_or_get(session, Tag, "test tag")

    assert tag.id is not None
    assert tag.name == "test tag"


def test_create_or_get_returns_existing_tag(session):
    tag = create_or_get(session, Tag, "test tag")
    tag_2 = create_or_get(session, Tag, "test tag")
    tag_3 = create_or_get(session, Tag, "  TEST    TAG   ")

    assert len(session.scalars(select(Tag)).all()) == 1
    assert tag.id == tag_2.id
    assert tag.id == tag_3.id
    assert tag.name == tag_2.name
    assert tag.name == tag_3.name
