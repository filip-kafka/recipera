from recipera_api.db.models import Recipe
from recipera_api.schemas.recipe import RecipeCreate
from recipera_api.services.slug import add_suffix, generate_slug
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


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
