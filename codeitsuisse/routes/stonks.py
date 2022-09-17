import logging
import json
from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)
@app.route("/stonks", methods=['POST'])
def sol():
    for case in request.get_json():
        energy = case['energy']
        print(f'{energy=}')
        captial = case['capital']
        print(f'{captial=}')
        timeline = {name:(val['price'],val['qty']) for name,val in case['timeline'].items()}
        for i,j in timeline.items():
            print(i, j)
        print("-"*30)