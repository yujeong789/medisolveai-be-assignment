from fastapi import APIRouter

from app.admin.doctor.router import router as doctor_router
from app.admin.treatment.router import router as treatment_router
from app.admin.hospital_slot.router import router as hospital_slot_router
from app.admin.appointment.router import router as appointment_router
from app.admin.statistics.router import router as statistics_router

router = APIRouter()

router.include_router(doctor_router)
router.include_router(treatment_router)
router.include_router(hospital_slot_router)
router.include_router(appointment_router)
router.include_router(statistics_router)