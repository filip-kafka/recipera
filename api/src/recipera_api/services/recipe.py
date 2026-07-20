from recipera_api.db.models import Recipe
from recipera_api.schemas.recipe import RecipeCreate
from recipera_api.services.helpers import add_suffix, generate_slug
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def create_recipe_service_(db: Session, payload: RecipeCreate) -> Recipe:
    # Resolve tags >> list[Tag] >> create_or_get for each
    # Resolve ingredients >> create or get for each ingredient name >> build RecipeIngredient with data
    # Build list[Steps] with position from array order
    # Construct Recipe with all the nested data attached + slug
    # Atomic commit in slug-collision retry loop
    ...


def create_recipe_service(db: Session, payload: RecipeCreate) -> Recipe:
    slug_base = generate_slug(payload.title)
    max_retries = 100 # arguably overkill for slug collision, but to keep on the safe side
    for i in range(max_retries):
        slug = slug_base if i == 0 else add_suffix(slug_base, i + 1)
        recipe = Recipe(
            title=payload.title,
            description=payload.description,
            servings=payload.servings,
            prep_time_min=payload.prep_time_min,
            cook_time_min=payload.cook_time_min,
            source=payload.source,
            slug=slug,
        )
        try:
            db.add(recipe)
            db.commit()
        except IntegrityError:
            # assumes slug is the only unique constraint
            # narrow by constraint name if others are added
            db.rollback()
            continue
        db.refresh(recipe)
        return recipe
    # 500 error for now, could be specified later to return user friendly HTTP error
    raise RuntimeError("Failed to generate unique slug")


def get_recipe_service(db: Session, recipe_id: int) -> Recipe | None:
    return db.get(Recipe, recipe_id)
