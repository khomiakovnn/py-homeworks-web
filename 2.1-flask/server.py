from flask import Flask
from flask import jsonify

app = Flask('app')


def test_page():
    return jsonify({'test': 'page'})


app.add_url_rule('/test_page/', view_func=test_page, methods=['GET'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
