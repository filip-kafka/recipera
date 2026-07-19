from datetime import datetime
from decimal import Decimal

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator


class StepCreate(BaseModel):
    text: str = Field(min_length=1)


class StepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    position: int
    text: str


class RecipeIngredientCreate(BaseModel):
    name: str = Field(min_length=1)
    quantity: str | None = None
    quantity_value: Decimal | None = None
    unit: str | None = None
    note: str | None = None


class RecipeIngredientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(validation_alias=AliasPath("ingredient", "name"))
    position: int
    quantity: str | None
    quantity_value: Decimal | None
    unit: str | None
    note: str | None


class RecipeBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    servings: int | None = Field(default=None)
    prep_time_min: int | None = Field(default=None)
    cook_time_min: int | None = Field(default=None)
    source: str | None = Field(default=None)


class RecipeCreate(RecipeBase):
    steps: list[StepCreate] = []
    ingredients: list[RecipeIngredientCreate] = []
    tags: list[str] = []


class RecipeRead(RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    steps: list[StepRead]
    ingredients: list[RecipeIngredientRead]
    tags: list[str]

    @field_validator("tags", mode="before")
    @classmethod
    def _validate_tags(cls, tags):
        return [tag.name if hasattr(tag, "name") else tag for tag in tags]
