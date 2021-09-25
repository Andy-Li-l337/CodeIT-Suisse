import logging
from flask import request, jsonify
from codeitsuisse import app
import hashlib
import math
logger = logging.getLogger(__name__)


@app.route('/cipher-cracking', methods=['POST'])
def crackCode():
    data = request.get_json()
    answer = "NULL"
    logger.info(data)
    for i in data:
        if i['est_mins'] < 0.5:
            f_x = math.ceil(math.log(int(i['X'])-1)*1000)/1000
            for k in range(10**(i['D'])):
                for g in range(1000000):
                    encodingstr = f"{k}::{g//1000}.{g%1000:0>3}"
                    shaed_data = hashlib.sha256(
                        encodingstr.encode('utf-8')).hexdigest()
                    if str(shaed_data) == str(i['Y']):
                        print("SOLUTION:", k, g/1000)
                        return str(data)
    return str(data)
