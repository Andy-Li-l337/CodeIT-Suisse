import logging
import json
from flask import request, jsonify
from scipy.stats import truncnorm
from codeitsuisse import app
import math
import numpy as np


logger = logging.getLogger(__name__)


@app.route('/optopt', methods=['POST'])
def calculate():
    data = request.get_json()
    options, gauss = data.get("options"), data.get("view")
    result = solve(options, gauss)
    return json.dumps(result)


def solve(options, gauss):
    gaussians = [truncnorm((i['min'] - i['mean']) / math.sqrt(i['var']), (i['max'] - i['mean']) /
                           math.sqrt(i['var']), loc=i['mean'], scale=math.sqrt(i['var'])) for i in gauss]
    rv = gaussians[0]
    x = np.linspace(rv.ppf(0.01), rv.ppf(0.99), 200)
    returns = [np.sum(np.multiply(rv.pdf(x), np.where(
        x < j['strike'], -1, x-(j['strike']+j['premium'])))) if j["type"] == "call" else np.sum(np.multiply(rv.pdf(x), np.where(
            x > j['strike'], -1, (j['strike']-j['premium'])-x))) for j in options]
    if max(returns) >= abs(min(returns)):
        ans = [100 if i == max(returns) else 0 for i in returns]
    else:
        ans = [-100 if i == min(returns) else 0 for i in returns]
    return ans
