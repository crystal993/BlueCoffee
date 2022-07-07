import jwt
from flask import request, render_template, redirect, Blueprint, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import config

client = MongoClient(config.DB_CLIENT)
db = client.dbtoy

bp = Blueprint('product', __name__, url_prefix='/product')


# 조회(R) : 상품 리스트
@bp.route('/list')
def product_list():
    # 상품 리스트 전체 찾기
    all_products = list(db.products.find({}))
    # 토큰을 받아와 로그인 여부 확인 및 유저 타입 확인
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        login_status = 1
        return render_template('product/list.html', login_status=login_status, user_info=user_info, all_products=all_products)
    else:
        login_status = 0
    return render_template('product/list.html', login_status=login_status, all_products=all_products)

# 조회(R) : 상품 등록 페이지로 이동
@bp.route('/form')
def product_form():
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

# 상세 페이지 이동 -> list.html -> detail.html
@bp.route('/detail/<id>')  # <a href="/product/detail/{{product._id}}">
def detail(id):
    # 각 product의 고유한 아이디 값으로 product의 정보를 받아온다. 
    # 각 product의 고유한 아이디 값으로 페이지에 접근 했으므로 
    # 고유 아이디가 Object 타입이므로 ObjectId 메서드를 사용해서 형변환
    product_info = db.products.find_one({"_id": ObjectId(id)})
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        login_status = 1
        return render_template('product/detail.html', login_status=login_status, product_info=product_info, user_info=user_info)
    else:
        login_status = 0
        return render_template('product/detail.html', login_status=login_status, product_info=product_info)

@bp.route('/edit/<id>')
def editForm(id):
    product_info = db.products.find_one({"_id": ObjectId(id)})
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        login_status = 1
        return render_template('product/update.html', login_status=login_status, product_info=product_info,
                               user_info=user_info)
    else:
        login_status = 0
        return render_template('product/update.html', login_status=login_status, product_info=product_info)



# 수정(U) : 상품 정보 수정
@bp.route('/edit', methods=['POST'])
def edit():
    img_url_receive = request.form['img_url_give']
    product_name_kor_receive = request.form['product_name_kor_give']
    product_name_eng_receive = request.form['product_name_eng_give']
    product_price_receive = request.form['product_price_give']
    product_detail_receive = request.form['product_detail_give']
    product_id_receive = request.form['product_id_give']

    db.products.update_one({'_id': ObjectId(product_id_receive)},{'$set':{'img_url':img_url_receive}})
    db.products.update_one({'_id': ObjectId(product_id_receive)},{'$set': {'product_name_kor': product_name_kor_receive}})
    db.products.update_one({'_id': ObjectId(product_id_receive)},{'$set':{'product_name_eng': product_name_eng_receive}})
    db.products.update_one({'_id': ObjectId(product_id_receive)},{'$set':{'product_price': product_price_receive}})
    db.products.update_one({'_id': ObjectId(product_id_receive)},{'$set':{'product_price': product_price_receive}})
    db.products.update_one({'_id': ObjectId(product_id_receive)},{'$set':{'product_detail': product_detail_receive}})
    return jsonify({'msg': '상품 수정 성공!'})
    


# 삭제(D) : 상품 삭제
@bp.route('/del/<id>')
def delete(id):
    db.products.delete_one({'_id':ObjectId(id)})
    return product_list()