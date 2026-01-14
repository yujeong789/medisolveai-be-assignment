from fastapi import FastAPI
from app.admin.router import router

app = FastAPI(title="Admin API")
app.include_router(router)