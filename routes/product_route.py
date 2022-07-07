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

# 등록(C): 상품 db에 저장
@bp.route('/add', methods=['POST'])
def add():
    img_url_receive = request.form['img_url_give']
    product_name_kor_receive = request.form['product_name_kor_give']
    product_name_eng_receive = request.form['product_name_eng_give']
    product_price_receive = request.form['product_price_give']
    product_detail_receive = request.form['product_detail_give']

    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})

        doc = {
            'writer' : user_info['user_id'],
            'img_url' : img_url_receive,
            'product_name_kor' : product_name_kor_receive,
            'product_name_eng' : product_name_eng_receive,
            'product_price' : product_price_receive,
            'product_detail' : product_detail_receive
        }

        db.products.insert_one(doc)
        return jsonify({'msg': '상품 등록 성공!'})
    else:
        return jsonify({'msg': '상품 등록 실패'})