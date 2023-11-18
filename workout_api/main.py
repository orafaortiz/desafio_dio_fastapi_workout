from fastapi import FastAPI
from fastapi_pagination import add_pagination

from workout_api.routers import api_router

app = FastAPI(title='Workout API')
add_pagination(app)
app.include_router(api_router)
