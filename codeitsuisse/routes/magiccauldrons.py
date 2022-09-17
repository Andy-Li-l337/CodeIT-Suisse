import logging
import json
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)
@app.route("/ /magiccauldrons", methods=['POST'])
def sol():
    
    output = []
    for case in request.get_json():
        for i in case.items():
            logger.info(i)
        logger.info("-"*30)
        part1sol = part1(case["part1"]["flow_rate"] * case["part1"]["time"], case["part1"]["row_number"], case["part1"]["col_number"])
        part2sol = part2(case["part2"]["flow_rate"] , case["part2"]["amount_of_soup"], case["part2"]["row_number"], case["part2"]["col_number"])
        part3sol = part3(case["part3"]["flow_rate"] * case["part3"]["time"], case["part3"]["row_number"], case["part3"]["col_number"])
        part4sol = part4(case["part4"]["flow_rate"] , case["part4"]["amount_of_soup"], case["part4"]["row_number"], case["part4"]["col_number"])
        output.append({"part1":part1sol,
        "part2":part2sol,
        "part3":part3sol,
        "part4":part4sol
        })
    return jsonify(output)
def part1(water,row,col):
    return round(hundredCauldronsSearch(water,row,col),2)
def part2(rate,amt,row,col):
    upT = 999
    lowT = 1
    newT = searchPart2(lowT,upT,rate,amt,row,col)
    low = hundredCauldronsSearch((newT-1)*rate,row,col)
    mid = hundredCauldronsSearch(newT*rate,row,col)
    up = hundredCauldronsSearch((newT+1)*rate,row,col) 
    print("DONE Searching")
    if amt < (low+mid)/2:
        return newT-1
    if (low+mid)/2 < amt < (mid+up)/2:
        return newT
    if amt > (mid+up)/2:
        return newT + 1
    if amt == (low+mid)/2:
        return newT-1 if newT % 2 else newT
    if amt == (mid+up)/2:
        return newT+1 if newT % 2 else newT  
def searchPart2(lowT,upT,rate,TargetAmt,row,col):
    condition = True
    step = 0
    while condition:
        midT = (lowT+upT)/2
        # print(lowT,midT,upT)
        # print(hundredCauldronsSearch(lowT*rate,row,col)- TargetAmt, (hundredCauldronsSearch(midT*rate,row,col) - TargetAmt))
        if (hundredCauldronsSearch(lowT*rate,row,col) - TargetAmt) * (hundredCauldronsSearch(midT*rate,row,col) - TargetAmt) < 0:
            upT = midT
        else:
            lowT = midT
        condition = abs(hundredCauldronsSearch(midT*rate,row,col) - TargetAmt) > 0.5 and step < 20
        step += 1
    return int(midT+0.5)
def part3(water,row,col):
    return round(hundredFiftyCauldronsSearch(water,row,col),2)

def part4(rate,amt,row,col):
    upT = 999
    lowT = 1
    newT = searchPart4(lowT,upT,rate,amt,row,col)
    low = hundredFiftyCauldronsSearch((newT-1)*rate,row,col)
    mid = hundredFiftyCauldronsSearch(newT*rate,row,col)
    up = hundredFiftyCauldronsSearch((newT+1)*rate,row,col)
    if amt < (low+mid)/2:
        return newT-1
    if (low+mid)/2 < amt < (mid+up)/2:
        return newT
    if amt > (mid+up)/2:
        return newT + 1
    if amt == (low+mid)/2:
        return newT-1 if newT % 2 else newT
    if amt == (mid+up)/2:
        return newT+1 if newT % 2 else newT  

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

def hundredCauldronsSearch(total,row,col):
    capacity = 100
    cauldrons = [[0 for x in range(500)] for y in range(500)] 
    cauldrons[0][0] = float(total)
    level = 0
    waterInLevel = True
    while(waterInLevel):
        waterInLevel = False
        for i in range(level+1):
            if cauldrons[level][i] > capacity:
                extraWater = cauldrons[level][i] - capacity
                try:
                    cauldrons[level][i] = capacity
                    cauldrons[level+1][i] += extraWater / 2
                    cauldrons[level+1][i+1] += extraWater / 2
                except:
                    raise OverflowError(level, i)
                waterInLevel = True
        level += 1
        #assert(level<300)
    return cauldrons[row][col]

def hundredFiftyCauldronsSearch(total,row,col):
    capacity = 100
    cauldrons = [[0 for x in range(500)] for y in range(500)] 
    cauldrons[0][0] = total
    level = 0
    waterInLevel = True
    while(waterInLevel):
        waterInLevel = False
        for i in range(level+1):
            if cauldrons[level][i] > capacity:
                extraWater = cauldrons[level][i] - capacity * (1 if level % 2 else 1.5)
                try:
                    cauldrons[level][i] = capacity
                    cauldrons[level+1][i] += extraWater / 2
                    cauldrons[level+1][i+1] += extraWater / 2
                except:
                    raise OverflowError(level, i)
                waterInLevel = True
        level += 1
        # print(level)
    return cauldrons[row][col]