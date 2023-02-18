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

class AdvertView(MethodView):

    def get(self, adv_id: int):
        print(adv_id)
        return jsonify({'HTTP_method': 'get'})

    def post(self):
        json_data = validate_adv_create(request.json)
        print(json_data)
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
        token = request.headers.get('token')
        print(adv_id, json_data, token)
        return jsonify({'HTTP_method': 'patch'})

    def delete(self, adv_id: int):
        token = request.headers.get('token')
        print(adv_id, token)
        return jsonify({'HTTP_method': 'delete'})


app.add_url_rule('/api/adverts/<int:adv_id>/',
                 view_func=AdvertView.as_view('adv_id'),
                 methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/api/adverts/',
                 view_func=AdvertView.as_view('no_id'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
