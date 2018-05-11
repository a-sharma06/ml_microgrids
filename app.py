# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 23:19:56 2018

@author: Akshay
"""

import requests

import pandas as pd
import numpy as np

import io
import os
import gc
import itertools

from flask import Flask, render_template, request, redirect

from bokeh.plotting import figure
from bokeh.palettes import Spectral11, Blues8, Spectral4
from bokeh.embed import components 
from bokeh.tile_providers import CARTODBPOSITRON_RETINA

from scipy.spatial.distance import pdist, squareform

import networkx as nx

import pyproj


#import matplotlib.pyplot as plt


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
    #bnames = ['a','b','c','d','e']
    #latitude= [40.729957,40.730223,40.730391,40.729780,40.729427]
    #longitude = [-73.998538,-73.998399, -73.998773,-73.997947,-73.997074]
    #types = ['office','residential','office','office','office']
    #area= [20000,5000,56000,456000,45006]
    bnames = request.form.getlist('name')
    area = request.form.getlist('area')
    latitude = request.form.getlist('latitude') 
    latitude = [float(x) for x in latitude]
    longitude = request.form.getlist('longitude')
    longitude = [float(x) for x in longitude]
    types = request.form.getlist('longitude')
    temp = latitude
    # original projection
    outProj = pyproj.Proj("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs")
    # resulting projection, WGS84, long, lat
    p =pyproj.Proj(init='epsg:4326')

    longitude, latitude = pyproj.transform(p,outProj,longitude, latitude)
    
    #latitude = [utm.from_latlon(lat, longitude[i])[0] for i, lat in enumerate(latitude)]
    #longitude = [utm.from_latlon(temp[i], lon)[1] for i, lon in enumerate(longitude)]
    #del(temp)
    
    data = {name : {'area': area[x], 'latitude': latitude[x], 'longitude': longitude[x], 'type': types[x]} for x,name in enumerate(bnames)}
    
    
    
    A = np.array(zip(latitude,longitude))
    B = squareform(pdist(A))
    
    pos = {x: (latitude[i], longitude[i]) for i,x in enumerate(list(bnames))}
    edges = [(row[0],row[1],pdist(np.array((pos[row[0]],pos[row[1]])))[0]) for row in list(itertools.combinations(bnames,2))]  
    
    H = nx.Graph()
    H.add_nodes_from(pos.keys())
    H.add_weighted_edges_from(edges)
    G = nx.minimum_spanning_tree(H)
    
    #path = list(nx.shortest_path(G))
    #path_edges = zip(path,path[1:])
    
    ys = [[data[edge[0]]['latitude'],data[edge[1]]['latitude']] for edge in list(G.edges())]
    xs = [[data[edge[0]]['longitude'],data[edge[1]]['longitude']] for edge in list(G.edges())]
    
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
    #OneHotEncoding
    
    p = figure(title = "Suggested Microgrid",plot_width=500, plot_height=500, x_axis_type="mercator", y_axis_type="mercator", 
               x_range = (min(longitude) -0.25*(max(longitude) - min(longitude)), max(longitude) + 0.25*(max(longitude) - min(longitude))),
               y_range = (min(latitude) -0.25*(max(latitude) - min(latitude)), max(latitude) + 0.25*(max(latitude) - min(latitude))))
               
    p.add_tile(CARTODBPOSITRON_RETINA)

    # add a circle renderer with a size, color, and alpha
    p.circle(longitude,latitude, size=10, color="navy")
    p.multi_line(xs, ys, color="firebrick", line_width=4)
    p.text(longitude, latitude, bnames)
    

    script, div = components(p)
    
    # show the results
    return render_template('about.html', script=script, div=div) 

if __name__ == '__main__':
   app.run(host='0.0.0.0')