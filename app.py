from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import config
import jwt

import routes.coffee_route as cr
import routes.mem_route as mr
import routes.product_route as pr

client = MongoClient(config.DB_CLIENT)
db = client.dbtoy

#플라스크 객체 생성
app = Flask(__name__)

#블루 프린트 등록
app.register_blueprint(mr.bp)
app.register_blueprint(pr.bp)
app.register_blueprint(cr.bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main')
def main():
    token_receive = request.cookies.get('mytoken')

    if token_receive is not None:
        # decoding
        payload = jwt.decode(token_receive, config.JWT_SECRET_KEY, algorithms=['HS256'])
        #  user_info = db.fin_users.find_one({"id": payload["id"]})
        login_status = 1
        return render_template('main.html', login_status=login_status)
    else:
        login_status = 0
        return render_template('main.html', login_status=login_status)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)