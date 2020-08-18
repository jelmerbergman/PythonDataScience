#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 22:31:27 2020

@author: jelmerbergman
"""

import os
import glob
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
os.chdir("/Users/jelmerbergman/downloads/data/Fitbit Data")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
#combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
#combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')


"""
"""
class display(object):
    """Display HTML representation of multiple objects"""
    template = """<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
    </div>"""
    def __init__(self, *args):
        self.args = args
        
    def _repr_html_(self):
        return '\n'.join(self.template.format(a, eval(a)._repr_html_())
                         for a in self.args)
    
    def __repr__(self):
        return '\n\n'.join(a + '\n' + repr(eval(a))
                           for a in self.args)

"""
"""




Fitbit1Data = pd.read_csv('/Users/jelmerbergman/downloads/data/Fitbit Data/combined_csv.csv')
Fitbit1Data['daydate'] = pd.to_datetime(Fitbit1Data['date']).dt.date
FitbitData = Fitbit1Data[Fitbit1Data.steps != 0]

Fitbit1Data = Fitbit1Data.set_index((pd.DatetimeIndex(Fitbit1Data['date'])))
#times = FitbitData.to_datetime(FitbitData.timestamp_col)
#FitbitData.groupby([times.hour, times.minute]).steps.sum()
#(pd.DatetimeIndex(FitbitData['date']))
#FitbitData.groupby(FitbitData.date.hour).mean()


"""
Onderstaande levert een draaitabel op. Is dit handig? 
"""
grouper = Fitbit1Data.groupby([pd.Grouper(freq='1H'), 'fitbit_id'])
result = grouper['steps'].sum().unstack('fitbit_id').fillna(0)

"""
Resample levert een hergroepering op op fitbitid, maar de fitbitid in de column wordt ook geaggregeerd, hoe kan die voorkomen worden? 
"""
Fitbit1DataHourly =  Fitbit1Data.groupby('fitbit_id').resample('1H', label='right').sum()



Fitbit1DataDaily =  Fitbit1Data.groupby('fitbit_id').resample('1D', label='right').sum()

def f(row):
    if row['steps'] >= 10000:
        val = 1
    
    else:
        val = 0
    return val

def f2(row):
    if row['steps'] > 0:
        val = 1
    
    else:
        val = 0
    return val

Fitbit1DataDaily['Goal'] = Fitbit1DataDaily.apply(f, axis=1)



Fitbit1DataDaily['Usable'] = Fitbit1DataDaily.apply(f2, axis=1)



Fitbit1DataHourly.boxplot()

Fitbit1DataHourly = Fitbit1DataHourly.drop(columns=[ 'fitbit_id'])
Fitbit1DataHourly.to_csv('/Users/jelmerbergman/downloads/data/Fitbit Data/combined_hourly_csv.csv')

Fitbit1DataHourly.boxplot(by="treatment_id", column = "steps")


FitbitAnalysisData = pd.read_csv('/Users/jelmerbergman/downloads/data/Fitbit Data/combined_hourly_csv.csv')
FitbitAnalysisData = FitbitAnalysisData.drop(columns=['treatment_id', 'fitbit_id.1'])


#Extraheer de datum uit de datetime
FitbitAnalysisData['day_date'] = pd.to_datetime(
    FitbitAnalysisData['date'],  errors='coerce'
).dt.floor('D')


#Kijk naar dagtotalen
FitbitAnalysisData['zero'] = FitbitAnalysisData.groupby(['fitbit_id','day_date'])['steps'].agg('sum')


print("Start de statistiek")
grp = Fitbit1DataHourly.groupby(['treatment_id']) 

print (grp.max()) 
print (grp.mean()) 
print (grp.count()) 

grph = Fitbit1DataDaily.groupby(['treatment_id']) 
print (grph.max()) 
print (grph.mean()) 
print (grph.count())  

print("Eindig de statistiek")
pivot = pd.pivot_table(Fitbit1DataHourly, values=["steps","calories","mets"], index=['treatment_id'], aggfunc=np.mean)
pivot.plot

#grouper = df.groupby([pd.Grouper(freq='1H'), 'Location'])
#result = grouper['Event'].count().unstack('Location').fillna(0)