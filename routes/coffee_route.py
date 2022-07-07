from flask import request, render_template, redirect, Blueprint, jsonify
from pymongo import MongoClient
import config

client = MongoClient(config.DB_CLIENT)
db = client.dbtoy

bp = Blueprint('cafe', __name__, url_prefix='/coffee')

# 조회(R) : 카페 리스트
@bp.route('/list')
def list():
    return render_template('coffee/list.html')
