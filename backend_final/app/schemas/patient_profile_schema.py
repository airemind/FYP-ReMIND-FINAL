from pydantic import BaseModel


class PatientProfileSchema(BaseModel):
    dob: str
    gender: str
    occupation: str
    marital_status: str
    family_description: str
    familiar_surroundings: str


class PatientProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    age: int
    gender: str
    occupation: str
    marital_status: str
    family_description: str
    familiar_surroundings: str

    class Config:
        from_attributes = True
