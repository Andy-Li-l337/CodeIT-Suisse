import logging
import json
import os
from flask import request, jsonify
from codeitsuisse import app

@app.route("/social-distancing", methods=["POST"])
@app.route("/ /social-distancing", methods=["POST"])
def socialDistancePermutation():
    return jsonify(["No Solution" for i in request.get_json()])