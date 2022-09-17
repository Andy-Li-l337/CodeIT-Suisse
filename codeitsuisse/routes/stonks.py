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
            portfolio={}
            for i,j in companyTimeline.items():
                print(i, j)
            
            def getMaxYearReturn(curYear,usableCapital,inventory = None):
                if inventory:
                    usableCapital += sum(timeline[curYear][com][0]*qty for com,qty in inventory.items() if com in timeline[curYear])
                deltaYearReturnTable = {}
                for targetYear in range(2037 - energy+1,2037):
                    pctChangeTable = {company:pctChange(timeline[curYear][company],timeline[targetYear][company]) for company in sorted(set(timeline.get(curYear,{}).keys()) & set(timeline.get(targetYear,{}).keys()))}
                    capitalAvailable = usableCapital
                    absReturn = 0
                    investments = dict()
                    orders = []
                    for company, change in sorted(pctChangeTable.items(),key=lambda k,v:v):
                        if capitalAvailable < min(timeline[curYear].values(),key= lambda x:x[0]):
                            break
                        investedCapital = capitalAvailable - capitalAvailable%timeline[curYear][company][0]
                        investments[company] = capitalAvailable // timeline[curYear][company][0]
                        orders.append(f"b-{company}-{investments[company]}")
                        absReturn += change*investedCapital
                        capitalAvailable -= investedCapital
                    deltaYearReturnTable[targetYear-curYear] = max(absReturn,0), investments, capitalAvailable, orders
                return deltaYearReturnTable
                #CHECK absReturn positive before using investments!
                #Possible Edge case: leftover money can be used to invest on small things
            initialInvestment = getMaxYearReturn(2037,capital)
            gotwobacktwoEarnings = initialInvestment.get(-2,[0])[0] + getMaxYearReturn(2035,capital+initialInvestment.get(-2,[0])[0]).get(2,[0])[0]
            gotwobackbackEarnings = initialInvestment.get(-2,[0])[0] + getMaxYearReturn(2035,capital+initialInvestment.get(-2,[0])[0]).get(1,[0])[0]
            gotwobackbackEarnings += getMaxYearReturn(2036,capital+gotwobackbackEarnings).get(1,[0])[0] 
            gogobackbackEarnings = initialInvestment.get(-1,[0])[0] + getMaxYearReturn(2036,capital+initialInvestment.get(-1,[0])[0]).get(-1,[0])[0]
            gogobackbackEarnings += getMaxYearReturn(2035,capital+gogobackbackEarnings).get(1,[0])[0]
            gogobackbackEarnings += getMaxYearReturn(2036,capital+gogobackbackEarnings).get(1,[0])[0]
            gogobacktwoEarnings =  initialInvestment.get(-1,[0])[0] + getMaxYearReturn(2036,capital+initialInvestment.get(-1,[0])[0]).get(-1,[0])[0]
            gogobacktwoEarnings += getMaxYearReturn(2035,capital+gogobackbackEarnings).get(2,[0])[0]
            gobackEarnings = initialInvestment.get(-1,[0])[0] + getMaxYearReturn(2036,capital+initialInvestment.get(-1,[0])[0]).get(1,[0])[0]
            gobackgobackEarnings = gobackEarnings * 2
            fourEnergy = (gotwobacktwoEarnings,gotwobackbackEarnings,gogobackbackEarnings,gobackgobackEarnings)
            if max(fourEnergy) > 0:
                if max(fourEnergy) == gotwobacktwoEarnings:
                    if initialInvestment.get(-2,[0,0,0,""])[0] > 0:
                        steps += initialInvestment.get(-2,[0,0,0,""])[3]
                    steps += "j-2037-2035"
                    if initialInvestment.get(-2,[0,0,0,""])[0] > 0:
                        for com,qty in initialInvestment.get(-2,[0,0,0,""])[2].items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2035,capital+initialInvestment.get(-2,[0])[0]).get(2,[0,0,0,""])[0] > 0:
                        steps += getMaxYearReturn(2035,capital+initialInvestment.get(-2,[0])[0]).get(2,[0,0,0,""])[3]
                    previousInvestment = getMaxYearReturn(2035,capital+initialInvestment.get(-2,[0])[0]).get(2,[0,0,0,""])[2]
                    steps += "j-2035-2037"
                    if getMaxYearReturn(2035,capital+initialInvestment.get(-2,[0])[0]).get(2,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"

                if max(fourEnergy) == gotwobackbackEarnings:
                    balance = 0
                    if initialInvestment.get(-2,[0,0,0,""])[0] > 0:
                        steps += initialInvestment.get(-2,[0,0,0,""])[3] 
                        balance = initialInvestment.get(-2,[0,0,0,""])[0]
                    steps += "j-2037-2035"
                    if initialInvestment.get(-2,[0,0,0,""])[0] > 0:
                        for com,qty in initialInvestment.get(-2,[0,0,0,""])[2].items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        balance += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0]
                        previousInvestment = getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[2]
                        steps += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[3]
                    steps += "j-2035-2036"
                    if getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                        previousInvestment = getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[2]
                        steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                    steps += "j-2036-2037"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
                if max(fourEnergy) == gogobackbackEarnings:
                    balance = 0
                    if initialInvestment.get(-1,[0,0,0,""])[0] > 0:
                        steps += initialInvestment.get(-1,[0,0,0,""])[3] 
                        balance = initialInvestment.get(-1,[0,0,0,""])[0]
                    steps += "j-2037-2036"
                    if initialInvestment.get(-1,[0,0,0,""])[0] > 0:
                        for com,qty in initialInvestment.get(-1,[0,0,0,""])[2].items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2036,capital+balance).get(-1,[0,0,0,""])[0] > 0:
                        steps += getMaxYearReturn(2036,capital+balance).get(-1,[0,0,0,""])[3]
                        previousInvestment = getMaxYearReturn(2036,capital+balance).get(-1,[0,0,0,""])[2]
                        balance += getMaxYearReturn(2036,capital+balance).get(-1,[0,0,0,""])[0]
                    steps += "j-2036-2035"
                    if getMaxYearReturn(2036,capital+balance).get(-1,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0]>0:
                        steps += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[3]
                        previousInvestment = getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[2]
                        balance += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0]
                    steps += "j-2035-2036"
                    if getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0]>0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                        previousInvestment = getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[2]
                        balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                    steps += "j-2036-2037"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
                if max(fourEnergy) == gobackgobackEarnings:
                    balance = 0
                    if initialInvestment.get(-1,[0,0,0,""])[0] > 0:
                        steps += initialInvestment.get(-1,[0,0,0,""])[3] 
                        balance = initialInvestment.get(-1,[0,0,0,""])[0]
                    steps += "j-2037-2036"
                    if initialInvestment.get(-1,[0,0,0,""])[0] > 0:
                        for com,qty in initialInvestment.get(-1,[0,0,0,""])[2].items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                        previousInvestment = getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[2]
                        balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                    steps += "j-2036-2037"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2037,capital+balance).get(-1,[0,0,0,""])[0] > 0:
                        steps += getMaxYearReturn(2037,capital+balance).get(-1,[0,0,0,""])[3]
                        previousInvestment = getMaxYearReturn(2037,capital+balance).get(-1,[0,0,0,""])[2]
                        balance += getMaxYearReturn(2037,capital+balance).get(-1,[0,0,0,""])[0]
                    steps += "j-2037-2036"
                    if getMaxYearReturn(2037,capital+balance).get(-1,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                        previousInvestment = getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[2]
                        balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                    steps += "j-2036-2037"
                    if getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0] > 0:
                        for com,qty in previousInvestment.items():
                            steps += f"s-{com}-{qty}"
            print("-"*30)
        output.append(steps)
        
    return jsonify(output)

def pctChange(old,new):
    return new/old