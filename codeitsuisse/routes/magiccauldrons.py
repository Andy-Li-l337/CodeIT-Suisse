import logging
import json
from flask import request, jsonify
from codeitsuisse import app
import time
import random
logger = logging.getLogger(__name__)
@app.route("/ /magiccauldrons", methods=['POST'])
def sol():
    startTime = time.time()
    output = []
    for case in request.get_json():
        for i in case.items():
            logger.info(i)
        logger.info("-"*30)
        part1sol = part1(case["part1"]["flow_rate"] * case["part1"]["time"], case["part1"]["row_number"], case["part1"]["col_number"])
        part2sol = part2(case["part2"]["flow_rate"] , case["part2"]["amount_of_soup"], case["part2"]["row_number"], case["part2"]["col_number"])
        part3sol = part3(case["part3"]["flow_rate"] * case["part3"]["time"], case["part3"]["row_number"], case["part3"]["col_number"])
        part4sol = part4(case["part4"]["flow_rate"] , case["part4"]["amount_of_soup"], case["part4"]["row_number"], case["part4"]["col_number"])
        output.append({"part1":0, #correct
        "part2":part2sol,
        "part3":0,
        "part4":part4sol
        })
        if time.time()-startTime > 3.2:
            break
    logger.info("*"*30)
    for i in output:
        logger.info(i)
    logger.info("*"*30)
    return jsonify(output)
def part1(water,row,col):
    return round(hundredCauldronsSearch(water,row,col),2)
def part2(rate,amt,row,col):
    upT = min((row+col+2)*100//rate,999)
    lowT = 1
    newT = searchPart2(lowT,upT,rate,amt,row,col)
    return round(newT)
def searchPart2(lowT,upT,rate,TargetAmt,row,col):
    condition = True
    step = 0
    while condition:
        midT = (lowT+upT)/2
        if (hundredCauldronsSearch(lowT*rate,row,col) - TargetAmt) * (hundredCauldronsSearch(midT*rate,row,col) - TargetAmt) < 0:
            upT = midT
        else:
            lowT = midT
        condition = abs(hundredCauldronsSearch(midT*rate,row,col) - TargetAmt) > 1 and step < 20
        step += 1
    return round(midT)
def part3(water,row,col):
    return round(hundredFiftyCauldronsSearch(water,row,col),2)

def part4(rate,amt,row,col):
    upT = 999
    lowT = 1
    newT = searchPart4(lowT,upT,rate,amt,row,col)
    return round(newT)

def searchPart4(lowT,upT,rate,TargetAmt,row,col):
    condition = True
    step = 0
    while condition:
        midT = (lowT+upT)/2
        # print(lowT,midT,upT)
        # print(hundredFiftyCauldronsSearch(lowT*rate,row,col)- TargetAmt, (hundredFiftyCauldronsSearch(midT*rate,row,col) - TargetAmt))
        if (hundredFiftyCauldronsSearch(lowT*rate,row,col) - TargetAmt) * (hundredFiftyCauldronsSearch(midT*rate,row,col) - TargetAmt) < 0:
            upT = midT
        else:
            lowT = midT
        condition = abs(hundredFiftyCauldronsSearch(midT*rate,row,col) - TargetAmt) > 0.5 and step < 20
        step += 1
    return int(midT+0.5)

def hundredCauldronsSearch(X, i, j):
    i,j = i+1,j+1
    glass = [0]*int(i *(i + 1) / 2)
    index = 0
    glass[index] = X
    capacity = 100
    for row in range(1,i):
        for col in range(1,row+1):
            X = glass[index]
            glass[index] = capacity if (X >= capacity) else X
            X = (X - 1) if (X >= capacity) else 0
            glass[index + row] += (X / 2)
            glass[index + row + 1] += (X / 2)
            index+=1
    return glass[int(i * (i - 1) /2 + j - 1)]

def hundredFiftyCauldronsSearch(X, i, j):
    i,j = i+1,j+1
    glass = [0]*int(i *(i + 1) / 2)
    index = 0
    glass[index] = X
    capacity = 100
    for row in range(1,i):
        for col in range(1,row+1):
            X = glass[index]
            glass[index] = (100 if i % 2 else 150) if (X >= (100 if i % 2 else 150)) else X
            X = (X - 1) if (X >= (100 if i % 2 else 150)) else 0
            glass[index + row] += (X / 2)
            glass[index + row + 1] += (X / 2)
            index+=1
    return glass[int(i * (i - 1) /2 + j - 1)]
