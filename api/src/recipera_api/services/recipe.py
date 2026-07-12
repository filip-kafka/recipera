from recipera_api.db.models import Recipe
from recipera_api.schemas.recipe import RecipeCreate
from sqlalchemy.orm import Session


def create_recipe_service(db: Session, payload: RecipeCreate) -> Recipe:
    recipe = Recipe(
        title=payload.title,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


def get_recipe_service(db: Session, recipe_id: int) -> Recipe | None:
    return db.get(Recipe, recipe_id)
