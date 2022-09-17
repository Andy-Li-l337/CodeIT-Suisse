import logging
import json
from flask import request, jsonify
from codeitsuisse import app

@app.route("/cryptocollapz", methods=['POST'])
def naive():
    output = []
    for inputList in request.get_json():
        outputList = []
        for elem in inputList:
            while elem != 1:
                maxValue = 1
                if elem % 2:
                    elem /= 2
                else:
                    elem = 4*elem + 3
                maxValue = max(elem, maxValue)
            maxValue.append(outputList)
        output.append(outputList)
    return jsonify(output)
