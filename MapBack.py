from flask import Flask, send_file
import os

from mapHandler import mark_from_db, mark_from_db_user

app = Flask(__name__)


@app.route('/garbage')
def pothole_map():
    mark_from_db()
    return send_file('html/map.html')


@app.route('/garbage/<int:user_id>')
def pothole_map_by_user_id(user_id):
    mark_from_db_user(user_id)
    return send_file(f'html/map{user_id}.html')


@app.route('/')
def index():
    return send_file('html/base.html')


if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
