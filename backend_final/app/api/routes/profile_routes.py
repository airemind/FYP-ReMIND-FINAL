from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.patient_profile_schema import (
    PatientProfileSchema,
    PatientProfileResponseSchema,
)
from app.services.profile.profile_service import create_patient_profile
from app.models.user import User

router = APIRouter(prefix="/profiles", tags=["Patient Profiles"])


@router.post("/setup")
def setup_patient_profiles(
    profiles: List[PatientProfileSchema],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    created = create_patient_profile(db, current_user.id, profiles)
    return {
        "message": "Patient profiles setup successfully",
        "patient_id": current_user.id,
        "created_profiles": created,
    }
