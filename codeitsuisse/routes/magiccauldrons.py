import logging
import json
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)
@app.route("/magiccauldrons", methods=['POST'])
def sol():
    logger.info(request.get_json())
    logger.info("-"*30)
    output = []
    for case in request.get_json():
        part1sol = part1(case["part1"]["flow_rate"] * case["part1"]["time"], case["part1"]["row_number"], case["part1"]["col_number"])
        part2sol = part2(case["part2"]["flow_rate"] , case["part2"]["amount_of_soup"], case["part2"]["row_number"], case["part2"]["col_number"])
        part3sol = part3(case["part3"]["flow_rate"] * case["part3"]["time"], case["part3"]["row_number"], case["part3"]["col_number"])
        part4sol = part4(case["part4"]["flow_rate"] , case["part4"]["amount_of_soup"], case["part4"]["row_number"], case["part4"]["col_number"])
        output.append({"part1":part1sol,
        "part2":part2sol,
        "part3":part3sol,
        "part4":part4sol})
    return output
def part1(water,row,col):
    cauldrons = [[0 for x in range(200)] for y in range(200)] 
    cauldrons[0][0] = float(water)
    level = 0
    waterInLevel = True
    capacity = 100
    while(waterInLevel):
        waterInLevel = False
        for i in range(level+1):
            if cauldrons[level][i] > capacity:
                extraWater = cauldrons[level][i] - capacity
                cauldrons[level][i] = capacity
                cauldrons[level][i] += extraWater / 2
                cauldrons[level][i+1] += extraWater / 2
                waterInLevel = True
        level += 1
    return round(cauldrons[row][col],2)
def part2(rate,amt,row,col):
    curamt = 0
    prevamt = 0
    t = 0
    capacity = 100
    while(prevamt < amt):
        t += 1
        prevamt = curamt
        cauldrons = [[0 for x in range(200)] for y in range(200)] 
        cauldrons[0][0] = float(rate*t)
        level = 0
        waterInLevel = True
        while(waterInLevel):
            waterInLevel = False
            for i in range(level+1):
                if cauldrons[level][i] > capacity:
                    extraWater = cauldrons[level][i] - capacity
                    cauldrons[level][i] = capacity
                    cauldrons[level][i] += extraWater / 2
                    cauldrons[level][i+1] += extraWater / 2
                    waterInLevel = True
            level += 1
        curamt = cauldrons[row][col]
    if amt > (curamt+prevamt)/2:
        return t
    if amt < (curamt+prevamt)/2:
        return t-1
    return t-1 if t % 2 else t
    
def part3(water,row,col):
    cauldrons = [[0 for x in range(200)] for y in range(200)] 
    cauldrons[0][0] = float(water)
    level = 0
    waterInLevel = True
    capacity = 100
    while(waterInLevel):
        waterInLevel = False
        for i in range(level+1):
            if cauldrons[level][i] > capacity:
                extraWater = cauldrons[level][i] - capacity * (1 if level % 2 else 1.5)
                cauldrons[level][i] = capacity * (1 if level % 2 else 1.5)
                cauldrons[level][i] += extraWater / 2
                cauldrons[level][i+1] += extraWater / 2
                waterInLevel = True
        level += 1
    return round(cauldrons[row][col],2)

def part4(rate,amt,row,col):
    curamt = 0
    prevamt = 0
    t = 0
    capacity = 100
    while(prevamt < amt):
        t += 1
        prevamt = curamt
        cauldrons = [[0 for x in range(200)] for y in range(200)] 
        cauldrons[0][0] = float(rate*t)
        level = 0
        waterInLevel = True
        while(waterInLevel):
            waterInLevel = False
            for i in range(level+1):
                if cauldrons[level][i] > capacity:
                    extraWater = cauldrons[level][i] - capacity * (1 if level % 2 else 1.5)
                    cauldrons[level][i] = capacity * (1 if level % 2 else 1.5)
                    cauldrons[level][i] += extraWater / 2
                    cauldrons[level][i+1] += extraWater / 2
                    waterInLevel = True
            level += 1
        curamt = cauldrons[row][col]
    if amt > (curamt+prevamt)/2:
        return t
    if amt < (curamt+prevamt)/2:
        return t-1
    return t-1 if t % 2 else t