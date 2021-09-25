import logging
from flask import request, jsonify
from codeitsuisse import app
import hashlib
import math
logger = logging.getLogger(__name__)


@app.route('/cipher-cracking', methods=['POST'])
def crackCode():
    data = request.get_json()
    for i in data:
        if i['est_mins'] < 0.5:
            f_x = math.ceil(math.log(2*i['X']-1)*1000)/1000
            for k in range(10**i['D']):
                encodingstr = f"{k}::{f_x}"
                shaed_data = hashlib.sha256(
                    encodingstr.encode('utf-8')).hexdigest()
                if str(shaed_data) == i['Y']:
                    print(k)
                    break
    return data
