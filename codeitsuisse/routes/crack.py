import logging
from flask import request, jsonify
from codeitsuisse import app
import hashlib
import math
import random
logger = logging.getLogger(__name__)


def findK(z):
    if(z['D'] <= 5):
        f_x = math.floor((0.99992841*math.log(int(z['X']))-0.4214743)*100)/100
        for k in range(10**(z['D'])):
            for j in range(-20, 20):
                encodingstr = f"{k}::{f_x+0.001*j:.3f}"
                shaed_data = hashlib.sha256(
                    encodingstr.encode('utf-8')).hexdigest()
                if str(shaed_data) == str(z['Y']):
                    print("SOLUTION:", z['X'], f"{f_x+0.001*j:.3f}", j)
                    return k
        print(z['X'], f_x, "FAILED")
    return 0


@ app.route('/cipher-cracking', methods=['POST'])
def crackCode():
    data = request.get_json()
    answer = "NULL"
    sol = []
    logger.info(data)
    for i in data:
        sol.append(findK(i))
    return tuple(sol)
