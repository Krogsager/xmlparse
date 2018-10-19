"""
developed for python 3.6
requires
https://pypi.org/project/xmltodict/
"""


import xmltodict
import csv
import time
import glob

spreadsheet = csv.writer(open('forecast_'+time.strftime("%Y%m%d-%H%M%S")+'.csv', 'w'), delimiter=',')
spreadsheet.writerow(["date", "temperature", "precipitation", "winddirection", "windspeed", "pressure", "symbol"])

def appendRow(strFile):
    with open(strFile) as fd:
        doc = xmltodict.parse(fd.read())

    if doc['weatherdata']['location']['name'] != 'Aarhus': #sanity check
        raise ValueError('Unexpected location!')
        print(doc['weatherdata']['location']['name'])


    timelist = doc['weatherdata']['forecast']['tabular']['time']

    if timelist.__len__() != 48:
        raise ValueError('Expected 48 elements')

    h6 = timelist[:6] #slice away the first 42 hours

    dates = []
    tempC = []
    pp = []
    windD = []
    windS = [] #in miles per second!?
    pressure = []
    symbol = []

    for hour in h6:
        dates.append(hour['@from'])
        tempC.append(hour['temperature']['@value'])
        pp.append(hour['precipitation']['@value'])
        windD.append(hour['windDirection']['@deg'])
        windS.append(hour['windSpeed']['@mps'])
        pressure.append(hour['pressure']['@value'])
        symbol.append(hour['symbol']['@name'])


    for da,te,pp,wd,ws,pr,sy in zip(dates,tempC,pp,windD,windS,pressure,symbol):
        #print(da,te,pp,wd,ws,pr,sy)
        spreadsheet.writerow([da, te, pp, wd, ws, pr, sy])

files = []
for file in glob.glob('*.xml'):
    files.append(file)

files.sort()

for file in files: appendRow(file)
print("Finished")