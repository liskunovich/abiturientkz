from pydantic import BaseModel, EmailStr, constr, UUID4


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=6)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=6)


class UserResponseSchema(BaseModel):
    id: UUID4
    email: str

    class Config:
        orm_mode = True


class UserPasswordLoginSchema(BaseModel):
    """_summary_

    User need to transfer this data to get access to API

    Args:
        email (EmailStr): user email
        password (str): user password
    """

    email: EmailStr
    password: str


class AuthResponseSchema(BaseModel):
    user_id: UUID4
    email: EmailStr
    access_token: str
    refresh_token: str | None
