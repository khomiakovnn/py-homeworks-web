from flask import Flask, jsonify, request
from flask.views import MethodView
from db import Advertisement, Session
from schema import validate_adv_create
from errors import HttpError

app = Flask('server')


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
        with Session() as session:
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
            for field, value in json_data.items():
                setattr(advert, field, value)
            session.add(advert)
            session.commit()
        return jsonify({
            'HTTP_method': 'patch',
            'Status': 'Advert have been patched',
        })

    def delete(self, adv_id: int):
        with Session() as session:
            advert = get_adv(adv_id, session)
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
                 view_func=AdvertView.as_view('no_id'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
