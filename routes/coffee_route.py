import jwt
from flask import request, render_template, redirect, Blueprint, jsonify
from pymongo import MongoClient
import config

client = MongoClient(config.DB_CLIENT)
db = client.dbtoy

bp = Blueprint('cafe', __name__, url_prefix='/coffee')

# 조회(R) : 카페 리스트
@bp.route('/list')
def list():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        # decoding
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        # user_info = db.users.find_one({"id": payload["id"]})
        login_status = 1
        return render_template('coffee/list.html', login_status=login_status)
    else :
        login_status = 0
        return render_template('coffee/list.html', login_status=login_status)
