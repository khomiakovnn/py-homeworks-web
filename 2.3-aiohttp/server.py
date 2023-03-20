from aiohttp import web
from sqlalchemy.exc import IntegrityError

from db import Advertisement, Session, User
from schema import validate_adv_create, validate_user_create
from errors import HttpError

app = web.Application()

if __name__ == '__main__':
    web.run_app(app)
