import logging
import json
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/optopt', methods=['POST'])
def calculate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    options, gauss = data.get("options"), data.get("view")
    result = solve(options, gauss)
    logging.info("Data returned", result)
    return result  # json.dumps(result)


def solve(options, gauss):
    i = gauss[0]
    # a, b = (i['min'] - i['mean'])/math.sqrt(i['var']
    #                                        ), (i['max'] - i['mean'])/math.sqrt(i['var'])
    #rv = truncnorm(a, b)
    #ev = rv.expect()
    option_ev = [(i['mean'] - j['strike']+j['premium']) if j['type'] ==
                 "call" else -(i['mean'] - j['strike']+j['premium']) for j in options]
    target = option_ev.index(max(option_ev)) if max(option_ev) > 0 else None
    return json.dumps([100] + [0]*(len(options)-1))
