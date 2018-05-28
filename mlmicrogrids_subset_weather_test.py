# -*- coding: utf-8 -*-
"""
Created on Sun May 27 17:08:12 2018

@author: Akshay
"""


#Code to generate some weather data for the actual model

lookback = 10
delay = 1 
max_index = None
min_index = 0 
batch_size = 100
step = 1

testweather = []

for x in range(1,len(building_info['building_id'].unique())*70/100):
    data = datasplit(processed_data[processed_data['building_id'] == random.choice(building_info['building_id'])])
    testweather_new, _ = generator_ml(data['X'], data['Y'], lookback, delay, max_index, min_index, batch_size, step)
    testweather += testweather_new

testweather = pd.concat(testweather)
testweather_df = pd.DataFrame(testweather)
testweather_df = testweather_df.fillna(0)
testweather_df.to_csv("testweather.csv")