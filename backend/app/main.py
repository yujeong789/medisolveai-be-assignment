from fastapi import FastAPI
from app.patient.main import app as patient_app
from app.admin.main import app as admin_app

app = FastAPI(title="API Gateway")

app.mount("/api/v1/patient", patient_app)
app.mount("/api/v1/admin", admin_app)
