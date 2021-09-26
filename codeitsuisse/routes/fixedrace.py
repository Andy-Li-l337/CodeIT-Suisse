import logging
import json
from flask import request, jsonify
from codeitsuisse import app
from codeitsuisse import people
logger = logging.getLogger(__name__)


@app.route('/fixedrace', methods=['POST'])
def counting():
    global people
    data = request.get_data(as_text=True)
    for i in data.split(","):
        if i not in people:
            people[i] = 0
        people[i] += 1
    people = {k: v for k, v in sorted(
        people.items(), key=lambda item: item[1], reverse=True)}
    peopleName = list(people.keys())
    peopleName = [x for x in people.keys() if x in data.split(",")]
    logger.info(people)
    return ",".join(peopleName[:10])


@app.route('/fixedrace', methods=['GET'])
def tester():
    return "Not Reachable"
