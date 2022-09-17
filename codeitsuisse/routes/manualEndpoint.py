import logging
import json
import os
from flask import request, jsonify
from codeitsuisse import app

@app.route("/manual", methods=["POST"])
def manualInput():
    output = []
    command = ""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Input:")
        print(request.get_json())
        if len(output) > 0:
            print("Current Buffer:")
            print(output[-1])
        command = input()
        if command == "UNDO":
            if len(output) > 0:
                output.pop()
            continue
        if command == "HIST":
            for i in output:
                print(i)
                print("-"*20)
            print("Press enter to continue")
            continue
        if command == "CLEAR":
            command = []
            continue
        if command == "END":
            break
        output.append(command+'\n')
    if len(output) > 0:
        return json.loads(output[-1])
    return jsonify({})