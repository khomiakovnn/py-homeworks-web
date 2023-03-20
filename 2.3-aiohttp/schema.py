from pydantic import BaseModel, ValidationError, validator
from errors import HttpError


class CreateAdv(BaseModel):
    title: str
    description: str
    author: int


class CreateUser(BaseModel):

    username: str
    password: str
    email: str

    @validator('password')
    def validate_password(cls, value: str):
        if len(value) < 3:
            raise ValueError('Password is less then 3 symbols')
        return value


def validate_adv_create(json_data):
    try:
        adv_schema = CreateAdv(**json_data)
        return adv_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())


def validate_user_create(json_data):
    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())
