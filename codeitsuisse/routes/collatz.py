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
            maxValue = 1
            while elem != 1:
                if elem % 2:
                    elem = 3*elem + 1
                else:
                    elem //= 2
                maxValue = max(elem, maxValue)
            outputList.append(maxValue)
        output.append(outputList)
    return jsonify(output)
