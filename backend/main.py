from fastapi import FastAPI
from backend.routes import router

app = FastAPI(
    title='Scientist-AI',
    version='0.1.0',
)
app.include_router(router)