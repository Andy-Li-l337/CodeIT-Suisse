import logging
from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)


@app.route('/cipher-cracking', methods=['POST'])
def crackCode():
    data = request.get_json()
    logger.info(data)
    return data
