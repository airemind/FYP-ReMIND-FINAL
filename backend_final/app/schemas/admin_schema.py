from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    admin_id: str
    password: str


class AdminUpdateUserRequest(BaseModel):
    username: str
    email: str
