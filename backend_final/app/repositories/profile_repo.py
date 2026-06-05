from sqlalchemy.orm import Session
from app.models.patient_profile import PatientProfile


def create_patient_profile_record(db: Session, data: dict):

    profile = PatientProfile(**data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
