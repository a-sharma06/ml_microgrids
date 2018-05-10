# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 23:19:56 2018

@author: Akshay
"""

import requests
import pandas as pd
import io
from bokeh.plotting import figure
from bokeh.palettes import Spectral11, Blues8
from flask import Flask, render_template, request, redirect
from bokeh.embed import components 
import os
import networkx as nx
from bokeh.models.graphs import from_networkx
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    #if request.method == 'POST':
        #ticker = request.form['ticker']
        #features = request.form['features']
        #return redirect("https://www.google.com")
        #return redirect(url_for('about'))
    return render_template('index.html')
    

@app.route('/about', methods=['GET', 'POST'])
def about():
    #ticker = 'GOOG'
    #ticker = request.form['ticker']
    bnames = request.form.getlist('name')
    area = request.form.getlist('area')
    latitude = request.form.getlist('latitude') 
    latitude = [float(x) for x in latitude]
    longitude = request.form.getlist('longitude')
    longitude = [float(x) for x in longitude]
    #data = [ {name : {'area': area[x], 'latitude': latitude[x], 'longitude': latitude[x]}} for x,name in enumerate(bnames)]
    
    data = {name : 'area' for x,name in enumerate(bnames)}
    #H = nx.Graph()
    #for x,name in enumerate(bnames):
    #    H.add_node(name, pos = (latitude[x],longitude[x]))

    #lookup = dict([('open','Open'),('close','Close'),('adj_close','Adj. Open'),('adj_open','Adj. Close')])
    #cols = [lookup[x] for x in features]
    #cols.append('Date')
    #url = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.csv?start_date=2017-01-01&end_date=2017-12-31&order=asc&api_key='+os.environ['QUANDL_KEY']
    #urlData = requests.get(url).content
    #rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    #rawData.Date = pd.to_datetime(rawData.Date)
    #rawData = rawData.loc[:,cols]
    #cols.remove('Date')
    ## create a new plot with a title and axis labels
    #p = figure(tools="pan,wheel_zoom,box_zoom,reset", title='Quandl WIKI EOD Stock Price - 2017 ', x_axis_label='Time', y_axis_label='Price', x_axis_type="datetime")

    ##i=0
    ## add a line renderer with legend and line thickness                                                                                                                                       
    ##for x in cols:
    ##    p.line(y = rawData[x], x = rawData.Date, legend = (ticker + ' ' + x + ' - Value'), line_width=2, line_color=Blues8[i])
    ##    i = i+1
    
    #for i,x in enumerate(cols,0):
    #    p.line(y = rawData[x], x = rawData.Date, legend = (ticker + ' ' + x + ' - Value'), line_width=2, line_color=Blues8[i])     

    #p.legend.location = "top_left"
    ##p.legend.click_policy="hide"

    #plot = figure(title="Networkx Integration Demonstration",
    #          tools="", toolbar_location=None)

    #graph = from_networkx(H, nx.spring_layout, scale=2, center=(0,0))
    #plot.renderers.append(graph)    
    #script, div = components(plot)
    
    # show the results
    return render_template('about.html',result = data, keys = data.keys()) #script=script, div=div, 

if __name__ == '__main__':
   app.run()