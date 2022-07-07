from flask import request, render_template, redirect, Blueprint, jsonify
from pymongo import MongoClient
import config

client = MongoClient(config.DB_CLIENT)
db = client.dbtoy

bp = Blueprint('product', __name__, url_prefix='/product')

# 조회(R) : 상품 리스트
@bp.route('/list')
def list():
    return render_template('product/list.html')