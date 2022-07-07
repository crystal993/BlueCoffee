from flask import request, render_template, redirect, Blueprint, jsonify
from pymongo import MongoClient
import config
import jwt
import datetime
import hashlib

client = MongoClient(config.DB_CLIENT)
db = client.dbtoy

bp = Blueprint('member', __name__, url_prefix='/member')

@bp.route('/login', methods=['POST'])
def login():
    # 요청한 id, pw
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    # 패스워드 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # db에 저장된 id, pw
    find_user = db.users.find_one({'user_id': id_receive, 'user_pw': pw_hash},{'_id':False})

    msg = ''
    result = ''
    # DB에 존재하면 로그인 성공
    if(find_user):
        # payload (정보)
        payload = {
            'id' : id_receive,
            # 로그인 24시간 유지(), utc 기준이므로 9시간 더하면 우리나라 시간, 9시간+24시간 = 33시간
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=33)
        }
        token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')
        msg = '로그인 성공!'
        result = 'success'
        return jsonify({'msg': msg, 'result':result, 'token':token})
    else:
        msg = '로그인 실패'
        result = 'fail'
        return jsonify({'msg':msg, 'result':result})

@bp.route('/join', methods=['POST'])
def join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    phone_receive = request.form['phone_give']
    type_receive = request.form['type_give']

    # Encrypt
    pw_encode = pw_receive.encode('utf-8')
    # 단방향 알고리즘, 해시함수
    pw_hash = hashlib.sha256(pw_encode).hexdigest()


    doc = {
        'user_id' : id_receive,
        'user_pw' : pw_hash,
        'user_name' : name_receive,
        'user_phone' : phone_receive,
        'user_type' : type_receive
    }

    db.users.insert_one(doc)
    return jsonify({'msg':'회원가입 완료'})
