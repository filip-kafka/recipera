from fastapi import APIRouter, Depends, HTTPException
from recipera_api.db.session import get_db
from recipera_api.schemas.recipe import RecipeCreate, RecipeRead
from recipera_api.services.recipe import create_recipe_service, get_recipe_service
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{recipe_id}", response_model=RecipeRead, status_code=200)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe_service(db=db, recipe_id=recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("", response_model=RecipeRead, status_code=201)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    return create_recipe_service(db=db, payload=recipe)
