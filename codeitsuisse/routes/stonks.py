import logging
import json
from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)
@app.route("/%20cryptocollapz", methods=['POST'])
def sol():
    pass