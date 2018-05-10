# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 23:19:56 2018

@author: Akshay
"""

import requests
import pandas as pd
import io
from bokeh.plotting import figure
from bokeh.palettes import Spectral11, Blues8, Spectral4
from flask import Flask, render_template, request, redirect
from bokeh.embed import components 
import os
import networkx as nx
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
import gc
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist, squareform
import numpy as np
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool


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
    bnames = request.form.getlist('name')
    area = request.form.getlist('area')
    latitude = request.form.getlist('latitude') 
    latitude = [float(x) for x in latitude]
    longitude = request.form.getlist('longitude')
    longitude = [float(x) for x in longitude]
    types = request.form.getlist('longitude')
    #data = [ {name : {'area': area[x], 'latitude': latitude[x], 'longitude': latitude[x]}} for x,name in enumerate(bnames)]
    

    A = np.array(zip(latitude,longitude))
    B = squareform(pdist(A))
    
    H = nx.from_numpy_matrix(B)
    path = list(nx.shortest_path(H,source=0))
    path_edges = zip(path,path[1:])
    pos = nx.spring_layout(H)
    
    G = nx.Graph()
    G.add_nodes_from(H)
    G.add_edges_from(path_edges, color='red')
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
    

    plot = figure(title="Building Microgrid Path",x_range=(-50,50), y_range=(-50,50), 
                  tools="pan,wheel_zoom,box_zoom,reset")

#    plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())
    
    graph_renderer  = from_networkx(G, nx.spring_layout, scale = 2, center=(0,0))
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])
    
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)
    
    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = EdgesAndLinkedNodes()

   
    plot.renderers.append(graph_renderer)    
    script, div = components(plot)
    
    # show the results
    return render_template('about.html', script=script, div=div) 

if __name__ == '__main__':
   app.run(host='0.0.0.0')