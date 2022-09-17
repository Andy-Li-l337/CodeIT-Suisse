import logging
import json
from flask import request, jsonify
from codeitsuisse import app
from functools import reduce
logger = logging.getLogger(__name__)
@app.route("/%20stonks", methods=['POST'])
@app.route("/ stonks", methods=['POST'])
def stonkSolve():
    output = []
    for case in request.get_json():
        steps = []
        energy = case['energy']
        print(f'{energy=}')
        capital = case['capital']
        print(f'{capital=}')
        if energy <= 4:
            timeline = { year:{name:(val['price'],val['qty']) for name,val in com.items()} for year,com in case['timeline'].items()}
            companyNames = sorted(reduce(lambda x,y:x|y,[set(timeline[yr].keys()) for yr in timeline]))
            companyTimeline = {name:{year:(timeline[year][name][0],timeline[year][name][1]) for year in timeline if name in timeline[year]} for name in companyNames}
            #companyQuotes = {name:{timeline['price']:(year,timeline['qty']) for year in timeline if name in timeline[year]} for name in companyNames}
            
            for i,j in companyTimeline.items():
                print(i, j)
            
            def getMaxYearReturn(curYear,usableCapital):
                deltaYearReturnTable = {}
                for targetYear in range(2037 - energy+1,2037):
                    pctChangeTable = {company:pctChange(timeline[curYear][company],timeline[targetYear][company]) for company in sorted(set(timeline.get(curYear,{}).keys()) & set(timeline.get(targetYear,{}).keys()))}
                    capitalAvailable = usableCapital
                    absReturn = 0
                    for company, change in sorted(pctChangeTable.items(),key=lambda k,v:v):
                        if capitalAvailable < min(timeline[curYear].values(),key= lambda x:x[0]):
                            break
                        investedCapital = capitalAvailable - capitalAvailable%timeline[curYear][company]
                        absReturn += change*investedCapital
                        capitalAvailable -= investedCapital
                    deltaYearReturnTable[targetYear-curYear] = absReturn/capital
                return deltaYearReturnTable
            nowYear = 2037
            yearYield = getMaxYearReturn(nowYear,capital)
            highestReturnOption = max(yearYield, key=lambda key: yearYield[key])
            if yearYield[highestReturnOption] > 0:
                    
            

                
            print("-"*30)
        output.append(steps)
        
    return jsonify(output)

def pctChange(old,new):
    return new/old - 1