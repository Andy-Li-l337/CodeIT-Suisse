import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def solve(testCases):
    for t in testCases:
        solarr = {}
    return outstr


@app.route('/asteroid', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("test_cases")
    result = solve(inputValue)
    return json.dumps(result)
