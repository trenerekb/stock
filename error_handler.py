from flask import jsonify

from app import app


@app.errorhandler(422)
def error_handler(err):
    headers = err.data.get('header', None)
    message = err.data.get('message', ['Invalid request'])
    if headers:
        return jsonify({'message': message}), 400, headers

    return jsonify({'message': message}), 400