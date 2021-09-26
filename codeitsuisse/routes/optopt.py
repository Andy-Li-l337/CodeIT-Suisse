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
    returns = [optReturnForDists(gaussians, j) for j in options]
    print(returns)
    ans = [0] * len(returns)
    if max(returns) >= abs(min(returns)):
        ans[returns.index(max(returns))] = 100
    else:
        ans[returns.index(min(returns))] = -100
    return ans


def optReturnForDists(dists, option):
    sample_size = 4000
    totalWeight = sum(list(dists.values()))
    random_idx = np.random.choice(np.arange(len(dists)), size=(sample_size,), p=[
        v/totalWeight for v in dists.values()])
    data = np.zeros((sample_size, len(dists)))
    for idx, distr in enumerate(list(dists.keys())):
        data[:, idx] = distr.rvs(size=sample_size)
    sample = data[np.arange(sample_size), random_idx]
    return optReturnForDist(sample, option)


def optReturnForDist(stockPrices, option):
    if option['type'] == "call":
        return np.matmul(stockPrices, np.where(
            stockPrices < option['strike'], -option['premium'], stockPrices-(option['strike']+option['premium'])).reshape(-1, 1))
    else:
        return np.matmul(stockPrices, np.where(
            stockPrices > option['strike'], -option['premium'], (option['strike']-option['premium'])-stockPrices).reshape(-1, 1))
