from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RecipeBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    servings: int | None = Field(default=None)
    prep_time_min: int | None = Field(default=None)
    cook_time_min: int | None = Field(default=None)
    source: str | None = Field(default=None)


class RecipeCreate(RecipeBase):
    pass


class RecipeRead(RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
