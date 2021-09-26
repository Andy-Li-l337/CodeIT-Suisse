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
    gaussians = {truncnorm((i['min'] - i['mean']) / math.sqrt(i['var']), (i['max'] - i['mean']) /
                           math.sqrt(i['var']), loc=i['mean'], scale=math.sqrt(i['var'])): i['weight'] for i in gauss}
    rv = list(gaussians.keys())[0]
    returns = [optReturn(rv, j) for j in options]
    ans = [0] * len(returns)
    if max(returns) >= abs(min(returns)):
        ans[returns.index(max(returns))] = 100
    else:
        ans[returns.index(min(returns))] = -100
    return ans


def optReturn(dist, option):
    x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), 100)
    if option['type'] == "call":
        np.multiply(np.transpose(dist.pdf(x)), np.where(
            x < option['strike'], -option['premium'], x-(option['strike']+option['premium'])))
    else:
        np.multiply(np.transpose(dist.pdf(x)), np.where(
            x > option['strike'], -option['premium'], (option['strike']-option['premium'])-x))
