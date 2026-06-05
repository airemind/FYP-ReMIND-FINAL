from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.profile_repo import create_patient_profile_record


def create_patient_profile(
    db: Session,
    user_id: int,
    profiles,
):
    created_profiles = []
    for profile in profiles:

        # Calculate Age
        dob = datetime.strptime(
            profile.dob,
            "%Y-%m-%d",
        )
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        # Build Profile Data
        data = {
            "user_id": user_id,
            "age": age,
            "gender": profile.gender,
            "occupation": profile.occupation,
            "marital_status": profile.marital_status,
            "family_description": (profile.family_description),
            "familiar_surroundings": (profile.familiar_surroundings),
        }

        # Create Profile
        created = create_patient_profile_record(
            db,
            data,
        )
        created_profiles.append(created)
    return created_profiles
