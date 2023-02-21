from pydantic import BaseModel, ValidationError
from errors import HttpError


class CreateAdv(BaseModel):
    title: str
    description: str
    author: str


class CreateUser(BaseModel):
    username: str
    password: str
    email: str


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
