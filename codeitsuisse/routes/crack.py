import logging
from flask import request, jsonify
from codeitsuisse import app
import hashlib
import math
import json
logger = logging.getLogger(__name__)


def findK(z):
    if(z['D'] <= 6 and int(z['challenge_no']) <= 29):
        f_x = math.floor((0.99993543*math.log(int(z['X']))-0.421614)*100)/100
        for k in range(10**(z['D'])+1):
            for j in range(10, -1, -1):
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
    for i in data:
        sol.append(findK(i))
    return json.dumps(sol)
