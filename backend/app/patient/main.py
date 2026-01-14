from fastapi import FastAPI
from app.patient.router import router

app = FastAPI(title="Patient API")
app.include_router(router)