import json
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from bcrypt import hashpw, gensalt, checkpw

from db import Advertisement, Session, User, engine, Base


app = web.Application()


def hash_password(password):
    hashed_password = hashpw(password.encode(), salt=gensalt()).decode()
    return hashed_password


async def orm_context(app):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@web.middleware
async def session_midleware(requests, handler):
    async with Session() as session:
        requests['session'] = session
        return await handler(requests)


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_midleware)


async def get_user(user_id, session):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(text=json.dumps({'Status': 'error', 'message': 'user not found'}),
                               content_type='application/json')
    return user


async def get_ad(ad_id, session):
    advert = await session.get(Advertisement, ad_id)
    if advert is None:
        raise web.HTTPNotFound(text=json.dumps({'Status': 'error', 'message': 'advert not found'}),
                               content_type='application/json')
    return advert


class UserView(web.View):

    async def get(self):
        session = self.request['session']
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, session)
        return web.json_response({
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'email': user.email,
        })

    async def post(self):
        session = self.request['session']
        json_data = await self.request.json()
        json_data['password'] = hash_password(json_data['password'])
        user = User(**json_data)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(text=json.dumps({'Status': 'error', 'message': 'user already exists'}),
                                   content_type='application/json')
        return web.json_response({
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'email': user.email,
        })

    async def patch(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.request['session'])
        json_data = await self.request.json()
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        for field, value in json_data.items():
            setattr(user, field, value)
        self.request['session'].add(user)
        await self.request['session'].commit()
        return web.json_response({
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'email': user.email,
        })

    async def delete(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.request['session'])
        await self.request['session'].delete(user)
        await self.request['session'].commit()
        return web.json_response({
            'Status': 'deleted',
            'username': user.username,
        })

class AdView(web.View):

    async def get(self):
        session = self.request['session']
        ad_id = int(self.request.match_info['ad_id'])
        advert = await get_ad(ad_id, session)
        return web.json_response({
            'id': advert.id,
            'title': advert.title,
            'description': advert.description,
            'author': advert.author,
        })

    async def post(self):
        session = self.request['session']
        json_data = await self.request.json()
        advert = Advertisement(**json_data)
        session.add(advert)
        await session.commit()
        return web.json_response({
            'id': advert.id,
            'title': advert.title,
            'description': advert.description,
            'author': advert.author,
        })

    async def patch(self):
        ad_id = int(self.request.match_info['ad_id'])
        advert = await get_ad(ad_id, self.request['session'])
        json_data = await self.request.json()
        if json_data['user_id'] != advert.author:
            return web.json_response({
                'Status': "Access is denied",
            })
        for field, value in json_data.items():
            setattr(advert, field, value)
        self.request['session'].add(advert)
        await self.request['session'].commit()
        return web.json_response({
            'Status': 'patched',

        })

    async def delete(self):
        ad_id = int(self.request.match_info['ad_id'])
        advert = await get_ad(ad_id, self.request['session'])
        json_data = await self.request.json()
        if json_data['user_id'] != advert.author:
            return web.json_response({
                'Status': "Access is denied",
            })
        await self.request['session'].delete(advert)
        await self.request['session'].commit()
        return web.json_response({
            'Status': 'deleted',
            'advert': advert.title,
        })


app.add_routes([
    web.post('/api/ads/', AdView),
    web.post('/api/users/', UserView),
    web.get('/api/ads/{ad_id:\d+}/', AdView),
    web.patch('/api/ads/{ad_id:\d+}/', AdView),
    web.delete('/api/ads/{ad_id:\d+}/', AdView),
    web.get('/api/users/{user_id:\d+}/', UserView),
    web.patch('/api/users/{user_id:\d+}/', UserView),
    web.delete('/api/users/{user_id:\d+}/', UserView),
])

if __name__ == '__main__':
    web.run_app(app)
