# -*- coding: utf-8 -*-
"""
Created on Sun May 27 19:37:33 2018

@author: Akshay
"""

import pandas as pd

bnames = ['a','b','c','d','e']
latitude= [40.729957,40.730223,40.930391,40.729780,40.729427]
longitude = [-73.998538,-73.998399, -73.998773,-73.997947,-73.997074]
types = ['office','office','office','office','office']
area= [24000,15000,25000,5,55000]

rows = [[bnames[x], area[x], latitude[x], longitude[x], types[x]] for x in range(0,len(bnames))]
inputdf = pd.DataFrame(rows)
inputdf = pd.DataFrame(rows, columns = ['bnames', 'area', 'latitude', 'longitude', 'type'])
inputdf['key'] = 1

weather = pd.read_csv('C:/Users/Akshay/Documents/GitHub/ml_microgrids/data/testweather.csv')
weather['key'] = 1

merge_df = pd.merge(weather, inputdf[['area', 'type', 'bnames', 'key']], on='key').drop('key', axis = 1)
testdata = merge_df.drop('bnames', axis = 1)

pkl_file = open('C:/Users/Akshay/Documents/GitHub/ml_microgrids/data/mlmicrogrid.pkl', 'rb')
rf2 = pickle.load(pkl_file)

lb = LabelBinarizer()
testdata['type'] = lb.fit_transform(testdata['type'])
pca = PCA(n_components=2)
testdata = pca.fit_transform(testdata)

inputdf = pd.merge(inputdf, 
                 pd.DataFrame({"bnames": merge_df['bnames'],
                      "predicted": rf2.predict(testdata) }).groupby('bnames').sum().reset_index(),
                on = "bnames").drop('key', axis =1)

coords = inputdf.as_matrix(columns=['latitude', 'longitude'])

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

for x in range(num_clusters):
    db2 = DBSCAN(eps=limit_pred, min_samples=1).fit(cluster_pred[x])
    cluster_labels2 = db2.labels_
    num_clusters2 = len(set(cluster_labels2))
    
    cluster_pred_sub = pd.Series([cluster_pred[x][cluster_labels2 == n] for n in range(num_clusters2)])
    clusters_loc_sub = pd.Series([clusters_loc[x][cluster_labels2 == n] for n in range(num_clusters2)])
    
    for y in range(num_clusters2):
        if len(clusters_loc_sub[y]) == 1:
            #passing the name of the building as string, the latitude, longitude as a tuple
            G.add_node(clusters_loc_sub[y][0][0], pos = tuple([clusters_loc_sub[y][0][1], clusters_loc_sub[y][0][2]]))
        if len(clusters_loc_sub[y]) > 1:
            H = nx.Graph() 
            pos = {clusters_loc_sub[y][z][0]: (clusters_loc_sub[y][z][1], clusters_loc_sub[y][z][2]) for z in range(len(clusters_loc_sub[y]))}
            edges = [(row[0],row[1],haversine(pos[row[0]],pos[row[1]])) for row in list(itertools.combinations(pos.keys(),2))]  
            
            H.add_nodes_from(pos.keys())
            H.add_weighted_edges_from(edges)
            H = nx.minimum_spanning_tree(H)
            G.add_nodes_from(H)
            G.add_edges_from(H.edges())

import matplotlib.pyplot as plt

nx.draw(G)
