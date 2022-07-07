import jwt
from flask import request, render_template, redirect, Blueprint, jsonify
from pymongo import MongoClient
import config

client = MongoClient(config.DB_CLIENT)
db = client.dbtoy

bp = Blueprint('product', __name__, url_prefix='/product')


# 조회(R) : 상품 리스트
@bp.route('/list')
def list():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        login_status = 1
        return render_template('product/list.html', login_status=login_status, user_info=user_info)
    else:
        login_status = 0
    return render_template('product/list.html', login_status=login_status)

# 조회(R) : 상품 등록 페이지로 이동
@bp.route('/form')
def form():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        login_status = 1
        return render_template('product/form.html', login_status=login_status, user_info=user_info)
    else:
        login_status = 0
    return render_template('product/form.html', login_status=login_status)
