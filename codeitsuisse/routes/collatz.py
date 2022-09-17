import logging
import json
from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)
@app.route("/%20cryptocollapz", methods=['POST'])
@app.route("/ cryptocollapz", methods=['POST'])
def naive():
    logger.info(request.get_json())
    #print(request.get_json())
    output = []
    lookupDict = {1:4}
    for inputList in request.get_json():
        for elem in inputList:
            if elem not in lookupDict:
                maxValue = elem
                newElem = elem
                while newElem not in lookupDict:
                    if newElem % 2:
                        newElem = 3*newElem + 1
                    else:
                        newElem //= 2
                    maxValue = max(newElem, maxValue)
                # logger.info(elem)
                lookupDict[elem] = max(maxValue,lookupDict[newElem])
        output.append([lookupDict[i] for i in inputList])
    return jsonify(output)
