import logging
import json

from flask import request, jsonify
from codeitsuisse import app

@app.route("/tickerStreamPart1", methods=['POST'])
def to_cumulative():
    #print(request.get_json())
    stream = request.get_json()["stream"]
    outList = []
    agg = dict()
    tickerList = dict()
    for i in stream:
        timestamp = int(i[:2]) * 60 + int(i[3:5])
        if timestamp not in agg:
            agg[timestamp] = dict()
        for a, b, c in zip(*([iter(i.split(",")[1:])] * 3)):
            agg[timestamp][a] = agg[timestamp].get(
                a, [0, 0])[0] + int(b), agg[timestamp].get(
                    a, [0, 0])[1] + oneDpToInt(c) * int(b)
            if a not in tickerList:
                tickerList[a] = [0, 0]
    for timeInfo, val in dict(sorted(agg.items())).items():
        res = f"{timeInfo//60:02}:{timeInfo%60:02}"
        for ticker, values in dict(sorted(val.items())).items():
            tickerList[ticker] = [
                sum(x) for x in zip(tickerList[ticker], values)
            ]
            res += f",{ticker},{tickerList[ticker][0]},{intToOneDp(tickerList[ticker][1])}"
        outList += [res]
    # return outList
    return jsonify({"output": outList})

# Assumption for part 2: Assume that trade done in the same minute and with the same ticker would only appear in the input once


@app.route("/tickerStreamPart2", methods=['POST'])
def to_cumulative_delayed() -> list:
    stream = request.get_json()['stream']
    quantity_block = request.get_json()['quantityBlock']
    outList = []
    agg = dict()
    tickerList = dict()
    for i in stream:
        timestamp = int(i[:2]) * 60 + int(i[3:5])
        if timestamp not in agg:
            agg[timestamp] = dict()
        for a, b, c in zip(*([iter(i.split(",")[1:])] * 3)):
            agg[timestamp][a] = agg[timestamp].get(
                a, [0, 0])[0] + int(b), agg[timestamp].get(
                    a, [0, 0])[1] + oneDpToInt(c) * int(b)
            if a not in tickerList:
                tickerList[a] = [[0, 0], 0]
    for timeInfo, val in dict(sorted(agg.items())).items():
        res = ""
        for ticker, values in val.items():
            tickerList[ticker] = [[
                sum(x) for x in zip(tickerList[ticker][0], values)
            ], tickerList[ticker][1]]

            if tickerList[ticker][0][
                    0] >= tickerList[ticker][1] + quantity_block:
                tickerList[ticker][1] = tickerList[ticker][0][0] - \
                    tickerList[ticker][0][0] % quantity_block
                residueValue = values[1]//values[0] * \
                    (tickerList[ticker][0][0] % quantity_block)
                res += f",{ticker},{tickerList[ticker][1]},{intToOneDp(tickerList[ticker][0][1]-residueValue)}"
        if res:
            outList += [f"{timeInfo//60:02}:{timeInfo%60:02}" + res]
    return jsonify({"output": outList})


def oneDpToInt(num: str) -> int:
    return int(num[:-2]) * 10 + int(num[-1])


def intToOneDp(num: int) -> str:
    return f"{num//10}.{num%10}"
