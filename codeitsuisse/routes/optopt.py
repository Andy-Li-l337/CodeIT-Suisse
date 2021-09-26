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
    logger.info(data)
    options, gauss = data.get("options"), data.get("view")
    result = solve(options, gauss)
    logger.info(result)
    return json.dumps(result)


def solve(options, gauss):
    gaussians = [(truncnorm((i['min'] - i['mean']) / math.sqrt(i['var']), (i['max'] - i['mean']) /
                            math.sqrt(i['var']), loc=i['mean'], scale=math.sqrt(i['var'])), i['weight']) for i in gauss]
    rv = gaussians[0][0]
    x = np.linspace(rv.ppf(0.0001), rv.ppf(0.9999), 1000)
    returns = [np.sum(np.multiply(averageStockProbability(gaussians, x), np.where(x < j['strike'], -j['premium'], x-(j['strike']+j['premium'])))) if j["type"] ==
               "call" else np.sum(np.multiply(averageStockProbability(gaussians, x), np.where(x > j['strike'], -j['premium'], (j['strike']-j['premium'])-x))) for j in options]
    ans = [0] * len(returns)
    if max(returns) >= abs(min(returns)):
        ans[returns.index(max(returns))] = 100
    else:
        ans[returns.index(min(returns))] = -100
    return ans


def averageStockProbability(gaussians, x):
    total = 0
    for _, w in gaussians:
        total += w
    return sum([np.multiply(i.pdf(x), weight)/total for i, weight in gaussians])
