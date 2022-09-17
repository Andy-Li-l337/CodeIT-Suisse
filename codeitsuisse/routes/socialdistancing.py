import logging
import json
import os
from flask import request, jsonify
from codeitsuisse import app

@app.route("/social-distancing")
@app.route("/ /social-distancing")
def socialDistancePermutation():
    return jsonify(["No Solution" for i in request.get_json()])