import logging
import json
from flask import request, jsonify
from codeitsuisse import app
from codeitsuisse import people
logger = logging.getLogger(__name__)


@app.route('/cipher-cracking', methods=['POST'])
def crackCode():
    data = request.get_json()
    logger.info(data)
    return data


@app.route('/cipher-cracking', methods=['GET'])
def tester():
    return "Reached cipher-cracking"
