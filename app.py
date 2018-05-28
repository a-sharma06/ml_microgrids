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

from sklearn.preprocessing import LabelBinarizer
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN

from haversine import haversine

import networkx as nx

import pyproj

import pickle


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
    
    #--------------
    # Reading weather data and creatinf test data
    #--------------
    
    rows = [[bnames[x], area[x], latitude[x], longitude[x], types[x]] for x in range(0,len(bnames))]
    inputdf = pd.DataFrame(rows)
    inputdf = pd.DataFrame(rows, columns = ['bnames', 'area', 'latitude', 'longitude', 'type'])
    inputdf['key'] = 1
    
    weather = pd.read_csv('C:/Users/Akshay/Documents/GitHub/ml_microgrids/data/testweather.csv')
    weather['key'] = 1
    
    merge_df = pd.merge(weather, inputdf[['area', 'type', 'bnames', 'key']], on='key').drop('key', axis = 1)
    testdata = merge_df.drop('bnames', axis = 1)
    names = merge_df['bnames']
    
    #---------------
    # Reprojecting the coordinates
    #---------------
    #delete:  temp = latitude
    
    # original projection
    outProj = pyproj.Proj("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs")
    # resulting projection, WGS84, long, lat
    p =pyproj.Proj(init='epsg:4326')

    longitude, latitude = pyproj.transform(p,outProj,longitude, latitude)
    
    #latitude = [utm.from_latlon(lat, longitude[i])[0] for i, lat in enumerate(latitude)]
    #longitude = [utm.from_latlon(temp[i], lon)[1] for i, lon in enumerate(longitude)]
    #del(temp)
    
    data = {name : {'area': area[x], 'latitude': latitude[x], 'longitude': longitude[x], 'type': types[x]} for x,name in enumerate(bnames)}
    
    
    
    #delete:  A = np.array(zip(latitude,longitude))
    #delete:  B = squareform(pdist(A))
    
    #-------------------
    # Loading the Machine Learning model from pickle
    #-------------------
    
    pkl_file = open('./data/mlmicrogrid.pkl', 'rb')
    rf2 = pickle.load(pkl_file)
    
    #--------------------
    # Pre-processing the input data
    lb = LabelBinarizer()
    testdata['type'] = lb.fit_transform(testdata['type'])
    pca = PCA(n_components=2)
    testdata = pca.fit_transform(testdata)
    
    inputdf = pd.merge(inputdf, 
                 pd.DataFrame({"bnames": merge_df['bnames'],
                      "predicted": rf2.predict(testdata) }).groupby('bnames').sum().reset_index(),
                on = "bnames").drop('key', axis =1)

    coords = inputdf.as_matrix(columns=['latitude', 'longitude'])
    
    #------------------
    # Location based clustering
    # ----------------
    kms_per_radian = 6371.0088
    epsilon = 0.5 / kms_per_radian
    
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    
    clusters_loc = pd.Series([inputdf.as_matrix(columns=['bnames','latitude', 'longitude'])[cluster_labels == n] for n in range(num_clusters)])
    cluster_pred = pd.Series([inputdf.as_matrix(columns=['predicted'])[cluster_labels == n] for n in range(num_clusters)])
    
    #Maintaining the limit of one cluster 1000 kW
    limit_pred = 700 
    
    G = nx.Graph()

    
    #-------------------
    # Creating the graph
    #-------------------
    #pos = {x: (latitude[i], longitude[i]) for i,x in enumerate(list(bnames))}
    #edges = [(row[0],row[1],pdist(np.array((pos[row[0]],pos[row[1]])))[0]) for row in list(itertools.combinations(bnames,2))]  
    
    #H = nx.Graph()
    #H.add_nodes_from(pos.keys())
    #H.add_weighted_edges_from(edges)
    #G = nx.minimum_spanning_tree(H)
    
    
    for x in range(num_clusters):
        db2 = DBSCAN(eps=limit_pred, min_samples=1).fit(cluster_pred[x])
        cluster_labels2 = db2.labels_
        num_clusters2 = len(set(cluster_labels2))
        
        #cluster_pred_sub = pd.Series([cluster_pred[x][cluster_labels2 == n] for n in range(num_clusters2)])
        clusters_loc_sub = pd.Series([clusters_loc[x][cluster_labels2 == n] for n in range(num_clusters2)])
    
        
        for y in range(num_clusters2):
            if len(clusters_loc_sub[y]) == 1:
                #passing the name of the building as string, the latitude, longitude as a tuple
                G.add_node(clusters_loc_sub[y][0][0], pos = tuple([clusters_loc_sub[y][0][1], clusters_loc_sub[y][0][2]]))
            if len(clusters_loc_sub[y]) > 2:
                H = nx.Graph() 
                pos = {clusters_loc_sub[y][z][0]: (clusters_loc_sub[y][z][1], clusters_loc_sub[y][z][2]) for z in range(len(clusters_loc_sub[y]))}
                edges = [(row[0],row[1],haversine(pos[row[0]],pos[row[1]])) for row in list(itertools.combinations(pos.keys(),2))]  
                
                H.add_nodes_from(pos.keys())
                H.add_weighted_edges_from(edges)
                H = nx.minimum_spanning_tree(H)
                G.add_nodes_from(H)
                G.add_edges_from(H.edges())

    #--------------------
    # Plotting the graph
    #--------------------
    ys = [[data[edge[0]]['latitude'],data[edge[1]]['latitude']] for edge in list(G.edges())]
    xs = [[data[edge[0]]['longitude'],data[edge[1]]['longitude']] for edge in list(G.edges())]
    
        
    p = figure(title = "Suggested Microgrid",plot_width=500, plot_height=500, x_axis_type="mercator", y_axis_type="mercator", 
               x_range = (min(longitude) -0.25*(max(longitude) - min(longitude)), max(longitude) + 0.25*(max(longitude) - min(longitude))),
               y_range = (min(latitude) -0.25*(max(latitude) - min(latitude)), max(latitude) + 0.25*(max(latitude) - min(latitude))))
               
    p.add_tile(CARTODBPOSITRON_RETINA)

    # add a circle renderer with a size, color, and alpha
    p.circle(longitude,latitude, size=20, color="coral")
    p.multi_line(xs, ys, color="dimgray", line_width=4)
    p.text(longitude, latitude, bnames)
    

    script, div = components(p)
    
    # show the results
    return render_template('about.html', script=script, div=div) 

if __name__ == '__main__':
   app.run(host='0.0.0.0')