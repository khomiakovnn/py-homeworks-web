from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from db import Advertisement, Session, User
from schema import validate_adv_create, validate_user_create
from errors import HttpError

app = Flask('server')
bcrypt = Bcrypt(app)

@app.errorhandler(HttpError)
def error_handler(error):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_adv(adv_id: int, session: Session):
    advert = session.query(Advertisement).get(adv_id)
    if advert is None:
        raise HttpError(404, 'Advert have not been found')
    return advert


def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'User have not been found')
    return user


class UserView(MethodView):

    def get(self, user_id: int):

        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'email': user.email,
                'creation_time': int(user.created_at.timestamp()),
            })

    def post(self):
        json_data = validate_user_create(request.json)
        json_data['password'] = bcrypt.generate_password_hash(json_data['password'].encode()).decode()
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'User already exist')
            return jsonify(
                {
                    'id': new_user.id,
                    'username': new_user.username,
                    'password': new_user.password,  # Для проверки работоспособности
                    'email': new_user.email,
                    'creation_time': int(new_user.created_at.timestamp()),
                }
            )

    def patch(self, user_id: int):
        json_data = request.json
        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
            return jsonify({
                'HTTP_method': 'patch',
                'Status': 'User have been patched',
            })

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
        return jsonify({
            'HTTP_method': 'delete',
            'Status': 'User have been deleted',
        })


class AdvertView(MethodView):

    def get(self, adv_id: int):
        with Session() as session:
            advert = get_adv(adv_id, session)
            return jsonify({
                'id': advert.id,
                'title': advert.title,
                'description': advert.description,
                'created_at': advert.created_at,
                'author': advert.author,
            })

    def post(self):
        json_data = validate_adv_create(request.json)
        author = json_data['author']
        with Session() as session:
            user = session.query(User).get(author)
            if user is None:
                raise HttpError(404, 'User have not been found')
            new_adv = Advertisement(**json_data)
            session.add(new_adv)
            session.commit()
            return jsonify(
                {
                    'id': new_adv.id,
                    'creation_time': int(new_adv.created_at.timestamp()),
                }
            )

    def patch(self, adv_id: int):
        json_data = request.json
        with Session() as session:
            advert = get_adv(adv_id, session)
            if advert.author != json_data['author']:
                raise HttpError(401, 'You do not have rights to this operation')
            for field, value in json_data.items():
                setattr(advert, field, value)
            session.add(advert)
            session.commit()
        return jsonify({
            'HTTP_method': 'patch',
            'Status': 'Advert have been patched',
        })

    def delete(self, adv_id: int):
        json_data = request.json
        with Session() as session:
            advert = get_adv(adv_id, session)
            if advert.author != json_data['author']:
                raise HttpError(401, 'You do not have rights to this operation')
            session.delete(advert)
            session.commit()
        return jsonify({
            'HTTP_method': 'delete',
            'Status': 'Advert have been deleted',
        })


app.add_url_rule('/api/adverts/<int:adv_id>/',
                 view_func=AdvertView.as_view('adv_id'),
                 methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/api/adverts/',
                 view_func=AdvertView.as_view('adv_no_id'),
                 methods=['GET', 'POST'])

app.add_url_rule('/api/users/<int:user_id>/',
                 view_func=UserView.as_view('user_id'),
                 methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/api/users/',
                 view_func=UserView.as_view('user_no_id'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
