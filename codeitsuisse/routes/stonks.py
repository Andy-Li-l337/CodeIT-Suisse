import logging
import json
from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)
@app.route("/%20stonks", methods=['POST'])
@app.route("/ stonks", methods=['POST'])
def stoneSolve():
    for case in request.get_json():
        energy = case['energy']
        print(f'{energy=}')
        captial = case['capital']
        print(f'{captial=}')
        timeline = { year:{name:(val['price'],val['qty']) for name,val in com.items()} for year,com in case['timeline'].items()}
        for i,j in timeline.items():
            print(i, j)
        print("-"*30)
    return jsonify({})