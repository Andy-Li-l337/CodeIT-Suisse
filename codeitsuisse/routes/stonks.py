import logging
import json
from flask import request, jsonify
from pygame import init
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
                    steps += initialInvestment.get(-2,[0,0,0,""])[3]
                    steps += "j-2037-2035"
                    steps += getMaxYearReturn(2035,capital+initialInvestment.get(-2,[0])[0]).get(2,[0,0,0,""])[3]
                if max(fourEnergy) == gotwobackbackEarnings:
                    steps += initialInvestment.get(-2,[0,0,0,""])[3] 
                    balance = initialInvestment.get(-2,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                if max(fourEnergy) == gogobackbackEarnings:
                    steps += initialInvestment.get(-1,[0,0,0,""])[3] 
                    balance = initialInvestment.get(-1,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2036,capital+balance).get(-1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2036,capital+balance).get(-1,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2035,capital+balance).get(1,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                if max(fourEnergy) == gobackgobackEarnings:
                    steps += initialInvestment.get(-1,[0,0,0,""])[3] 
                    balance = initialInvestment.get(-1,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2037,capital+balance).get(-1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2037,capital+balance).get(-1,[0,0,0,""])[0]
                    steps += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[3]
                    balance += getMaxYearReturn(2036,capital+balance).get(1,[0,0,0,""])[0]
                    

            # if initialInvestment.get(-1,1) <= 1 and initialInvestment.get(-2,1) <= 1: #If there are no good investment opportunity
            #     if initialInvestment.get(-1,1) > initialInvestment.get(-2,1):
            #         portfolio = initialInvestment[-1][1]
            #         capital = initialInvestment[-1][2]
            #         steps += initialInvestment[-1][3]
            #         for company in portfolio:
            #             if timeline[2036][company][0] > timeline[2035][company][1]:
            #                 steps += f"s-{company}-{portfolio[company]}"
            #                 del portfolio[company]
            #     elif initialInvestment.get(-2,1) > initialInvestment.get(-1,1)*max(getMaxYearReturn(2036,capital).get(-1,1),getMaxYearReturn(2036,capital).get(1,1),1):
            #         portfolio = initialInvestment[-2][1]
            #         capital = initialInvestment[-2][2]
            #         steps += initialInvestment[-2][3]
            
                    
            steps.append("j-2037-2036")
            return2036 = getMaxYearReturn(2036,capital) #See If 2036 Have good investment opportunity
            if return2036.get(-1,1) <=1 and return2036.get(-1,1) <=1:
                steps.append("j-2036-2035")

                # if return2036[0] <= 1 or getMaxYearReturn(2036,capital):
                #     steps.append("j-2036-2035")
                #     return2035 = getMaxYearReturn(2035,capital)
                #     if return2035[0] <= 1:#See If 2035 Have good investment opportunity
                #         output.append("")
                #         continue
                #     portfolio = {k: return2035[1].get(k, 0) + portfolio.get(k, 0) for k in set(return2035[1]) | set(portfolio)}
                #     capital = return2035[1][2]
                #     steps += return2035[1][3]
                #     steps.append("j-2035-2036")
                #     for company in portfolio.keys():
                #         if company not in timeline[2037].keys():
                #             steps += f"s-{company}-{portfolio[company]}"
                #         del portfolio[company]
                #     backReturn2036Sell = getMaxYearReturn(2036,capital,portfolio)
                #     backReturn2036NoSell = getMaxYearReturn(2036,capital)
                #     if backReturn2036Sell[1][0] > 1 and backReturn2036Sell[1][0]>backReturn2036NoSell[1][0]:
                #         for company in portfolio.keys():
                #             steps += f"s-{company}-{portfolio[company]}"
                #             del portfolio[company]
                #         portfolio = {k: backReturn2036Sell[1][1].get(k, 0) + portfolio.get(k, 0) for k in set(backReturn2036Sell[1][1]) | set(portfolio)}
                #         capital = backReturn2036Sell[1][2]
                #         steps += backReturn2036Sell[1][3]
                #     steps.append("j-2036-2037")
                #     for company in portfolio.keys():
                #         steps += f"s-{company}-{portfolio[company]}"
                #         del portfolio[company]
                


            print("-"*30)
        output.append(steps)
        
    return jsonify(output)

def pctChange(old,new):
    return new/old