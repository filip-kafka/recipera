from fastapi import FastAPI

from recipera_api.routers.recipes import router as recipes_router

app = FastAPI(title="Recipera")
app.include_router(recipes_router, prefix="/api/v1/recipes", tags=["recipes"])
