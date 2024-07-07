# -*- coding: utf-8 -*-
"""percolation_project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-DvTwnshsIOrn60FFGA_-KF_XbrdeRD0
"""

import math
import numpy as np
import pandas as pd
import streamlit as st
import builtins as bt
import matplotlib.pyplot as plt
from scipy.stats import poisson
from sklearn.cluster import DBSCAN

"""#FUNZIONI"""

#FUNZIONE CHE GENERA COORDINATE CON UNA POIS LAMBA * T^2

def generate_poisson_coordinates(T, k):
  # Step 1: Generate N from Poisson distribution
  N = np.random.poisson(k * T**2)
  # Step 2: Check if N is zero and handle termination
  if N == 0:
    return []
  # Step 3: Generate random numbers and scale to coordinates
  else:
    coordinates_x = []
    coordinates_y = []
    for _ in range(N):
      U = np.random.random()
      V = np.random.random()
      coordinates_x.append(U * T)
      coordinates_y.append(V * T)
  #print (f"N = {N} \nCoordinates X = {coordinates_x} \nCoordinates Y = {coordinates_y}")
  return coordinates_x, coordinates_y, N

#FUNZIONE CHE CREA CLUSTERS
def clusterizza_dbscan(coordinates_x, coordinates_y, eps=1, min_samples=1):
# Combine x and y coordinates into a single NumPy array
  coordinates = np.array(list(zip(coordinates_x, coordinates_y)))

  # Create a DBSCAN instance with specified parameters
  db = DBSCAN(eps=eps, min_samples=min_samples)

  # Fit the model to the data points
  db.fit(coordinates)

  # Extract cluster labels for each point
  cluster_labels = db.labels_

  # Create a list to store clusters (indices of points in each cluster)
  clusters = []
  for i, label in enumerate(cluster_labels):
    # Skip noise points (labeled -1)
    if label == -1:
      continue
    # Find all points with the same label (belonging to the same cluster)
    cluster_indices = [j for j, l in enumerate(cluster_labels) if l == label]
    clusters.append(cluster_indices)

  return clusters

def remove_duplicates(clusters_with_doubles):
  for i in range(len(clusters_with_doubles)):
    for j in range(i+1, len(clusters_with_doubles)):
      if clusters_with_doubles[i] == clusters_with_doubles[j]:
        clusters_with_doubles[j] = "duplicato"
  clusters = []
  for element in clusters_with_doubles:
    if element != "duplicato":
      clusters.append(element)
  return clusters

#FUNZIONE PER SIZE DEL CLUSTER PIU GRANDE
def largest_cluster_size (clusters):
  max_cluster_size = 0
  for cluster in clusters:
    if len(cluster) > max_cluster_size:
      max_cluster_size = len(cluster)
  return max_cluster_size

#FUNZIONE CHE RESTITUISCE IL NUMERO DI CLUSTERS
def number_of_clusters(clusters):
  return len(clusters)

"""#SVOLGIMENTO"""

#coordinates_x, coordinates_y = generate_poisson_coordinates(T, l)

#clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
#clusters = remove_duplicates(clusters_with_duplicates)
#print(clusters)

#largest_cluster_size(clusters)

#number_of_clusters(clusters)

"""#ITERAZIONI

##LAMBDA = ?
"""

#T = int(bt.input('Inserisci la dimenzione massima del dominio(max suggested = 40): '))
#l = float(bt.input('Inserisci il valore di  λ (max suggested = 2): '))
#M = int(bt.input('Inserisci il nummero iterazioni M: '))


T = 20 #MAX DOMINIO
l = 1 #LAMBDA
M = 10 #NUMERO ITERAZIONI

#ITERAZIONI E CREAZIONE DFs
largest_cluster_size_df_0 = []
number_of_clusters_df_0 = []
number_of_ponits_df_0 = []
for i in range(M):
  coordinates_x, coordinates_y, N = generate_poisson_coordinates(T, l)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  #print ('Iteration: ', i+1, '\nNumber of points: ', N, '\nNumber of clusters: ',  number_of_clusters(clusters), '\nLargest cluster size: ', largest_cluster_size(clusters), '\n')
  largest_cluster_size_df_0.append(largest_cluster_size(clusters))
  number_of_clusters_df_0.append(number_of_clusters(clusters))
  number_of_ponits_df_0.append(N)

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_ponits_df_0, color = 'cadetblue')
plt.title('Number Of Points')
plt.xlabel('Iteration')
plt.ylabel('Number Of Points')

plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), largest_cluster_size_df_0, color = 'maroon')
plt.title('Largest Cluster Size')
plt.xlabel('Iteration')
plt.ylabel('Largest Cluster Size')
plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_clusters_df_0, color = 'forestgreen')
plt.title('Number of Clusters')
plt.xlabel('Iteration')
plt.ylabel('Number of Clusters')

plt.show()

clusters_info_0 = pd.Series(largest_cluster_size_df_0, name = 'largest_cluster_size')
clusters_info_0 = pd.concat([pd.Series(number_of_ponits_df_0, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_0, name = 'number_of_clusters'), clusters_info_0], axis = 1)

clusters_info_0.describe()

mean_largest_cluster_size_0 = np.mean(largest_cluster_size_df_0)
mean_number_of_clusters_0 = np.mean(number_of_clusters_df_0)
print("Mean of the largest cluster's size = ", mean_largest_cluster_size_0, "\nMean of the number of clusters = ", mean_number_of_clusters_0)

# Create a list to store colors for each cluster
cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

# Create a scatter plot with points colored by cluster
plt.figure(figsize = (5, 5))
for i, cluster in enumerate(clusters):
  x_values = [coordinates_x[index] for index in cluster]
  y_values = [coordinates_y[index] for index in cluster]
  plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)])
plt.xticks(range(0, T + 1, int(T/10)))
plt.yticks(range(0, T + 1, int(T/10)))
plt.show()

"""##PUNTO 1

###LAMBDA = 4.512/4PI
"""

T = 20 #MAX DOMINIO
l = 4.512/(4*math.pi) #LAMBDA
M = 200 #NUMERO ITERAZIONI

largest_cluster_size_df_1 = []
number_of_clusters_df_1 = []
number_of_ponits_df_1 = []

for i in range(M):
  coordinates_x, coordinates_y, N = generate_poisson_coordinates(T, l)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  #print ('Iteration: ', i+1, '\nNumber of points: ', N, '\nNumber of clusters: ',  number_of_clusters(clusters), '\nLargest cluster size: ', largest_cluster_size(clusters), '\n')
  largest_cluster_size_df_1.append(largest_cluster_size(clusters))
  number_of_clusters_df_1.append(number_of_clusters(clusters))
  number_of_ponits_df_1.append(N)

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_ponits_df_1, color = 'cadetblue')
plt.title('Number Of Points')
plt.xlabel('Iteration')
plt.ylabel('Number Of Points')

plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), largest_cluster_size_df_1, color = 'maroon')
plt.title('Largest Cluster Size')
plt.xlabel('Iteration')
plt.ylabel('Largest Cluster Size')
plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_clusters_df_1, color = 'forestgreen')
plt.title('Number of Clusters')
plt.xlabel('Iteration')
plt.ylabel('Number of Clusters')

plt.show()

clusters_info_1 = pd.Series(largest_cluster_size_df_1, name = 'largest_cluster_size')
clusters_info_1 = pd.concat([pd.Series(number_of_ponits_df_1, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_1, name = 'number_of_clusters'), clusters_info_1], axis = 1)

clusters_info_1.describe()

# Create a list to store colors for each cluster
cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

# Create a scatter plot with points colored by cluster
plt.figure(figsize = (5, 5))
for i, cluster in enumerate(clusters):
  x_values = [coordinates_x[index] for index in cluster]
  y_values = [coordinates_y[index] for index in cluster]
  plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)])
plt.xticks(range(0, T + 1, int(T/10)))
plt.yticks(range(0, T + 1, int(T/10)))
plt.show()

"""###LAMBDA > 4.512/4PI"""

T = 20 #MAX DOMINIO
l = 4.512/(2*math.pi) #LAMBDA
M = 200 #NUMERO ITERAZIONI

largest_cluster_size_df_2 = []
number_of_clusters_df_2 = []
number_of_ponits_df_2 = []

for i in range(M):
  coordinates_x, coordinates_y, N = generate_poisson_coordinates(T, l)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  #print ('Iteration: ', i+1, '\nNumber of points: ', N, '\nNumber of clusters: ',  number_of_clusters(clusters), '\nLargest cluster size: ', largest_cluster_size(clusters), '\n')
  largest_cluster_size_df_2.append(largest_cluster_size(clusters))
  number_of_clusters_df_2.append(number_of_clusters(clusters))
  number_of_ponits_df_2.append(N)

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_ponits_df_2, color = 'cadetblue')
plt.title('Number Of Points')
plt.xlabel('Iteration')
plt.ylabel('Number Of Points')

plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), largest_cluster_size_df_2, color = 'maroon')
plt.title('Largest Cluster Size')
plt.xlabel('Iteration')
plt.ylabel('Largest Cluster Size')

plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_clusters_df_2, color = 'forestgreen')
plt.title('Number of Clusters')
plt.xlabel('Iteration')
plt.ylabel('Number of Clusters')

plt.show()

clusters_info_2 = pd.Series(largest_cluster_size_df_2, name = 'largest_cluster_size')
clusters_info_2 = pd.concat([pd.Series(number_of_ponits_df_2, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_2, name = 'number_of_clusters'), clusters_info_2], axis = 1)

clusters_info_2.describe()

# Create a list to store colors for each cluster
cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

# Create a scatter plot with points colored by cluster
plt.figure(figsize = (5, 5))
for i, cluster in enumerate(clusters):
  x_values = [coordinates_x[index] for index in cluster]
  y_values = [coordinates_y[index] for index in cluster]
  plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)])
plt.xticks(range(0, T + 1, int(T/10)))
plt.yticks(range(0, T + 1, int(T/10)))
plt.show()

"""###LAMBDA < 4.512/4PI"""

T = 20 #MAX DOMINIO
l = 4.512/(8*math.pi) #LAMBDA
M = 200 #NUMERO ITERAZIONI

largest_cluster_size_df_3 = []
number_of_clusters_df_3 = []
number_of_ponits_df_3 = []

for i in range(M):
  coordinates_x, coordinates_y, N = generate_poisson_coordinates(T, l)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
  clusters = remove_duplicates(clusters_with_duplicates)
  #print ('Iteration: ', i+1, '\nNumber of points: ', N, '\nNumber of clusters: ',  number_of_clusters(clusters), '\nLargest cluster size: ', largest_cluster_size(clusters), '\n')
  largest_cluster_size_df_3.append(largest_cluster_size(clusters))
  number_of_clusters_df_3.append(number_of_clusters(clusters))
  number_of_ponits_df_3.append(N)

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_ponits_df_3, color = 'cadetblue')
plt.title('Number Of Points')
plt.xlabel('Iteration')
plt.ylabel('Number Of Points')

plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), largest_cluster_size_df_3, color = 'maroon')
plt.title('Largest Cluster Size')
plt.xlabel('Iteration')
plt.ylabel('Largest Cluster Size')

plt.show()

plt.figure(figsize = (10, 5))
plt.bar(range(M), number_of_clusters_df_3, color = 'forestgreen')
plt.title('Number of Clusters')
plt.xlabel('Iteration')
plt.ylabel('Number of Clusters')

plt.show()

clusters_info_3 = pd.Series(largest_cluster_size_df_3, name = 'largest_cluster_size')
clusters_info_3 = pd.concat([pd.Series(number_of_ponits_df_3, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_3, name = 'number_of_clusters'), clusters_info_3], axis = 1)

clusters_info_3.describe()

# Create a list to store colors for each cluster
cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

# Create a scatter plot with points colored by cluster
plt.figure(figsize = (5, 5))
for i, cluster in enumerate(clusters):
  x_values = [coordinates_x[index] for index in cluster]
  y_values = [coordinates_y[index] for index in cluster]
  plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)])
plt.xticks(range(0, T + 1, int(T/10)))
plt.yticks(range(0, T + 1, int(T/10)))
plt.show()

"""###CONFRONTO"""

confronta_largest_cluster_size_serie = pd.concat([pd.Series(largest_cluster_size_df_1, name = 'largest_cluster_size_df_λ=λc'), pd.Series(largest_cluster_size_df_2, name = 'largest_cluster_size_df_λ>λc'), pd.Series(largest_cluster_size_df_3, name = 'largest_cluster_size_df_λ<λc'), ], axis = 1)
confronta_largest_cluster_size_array = [np.mean(largest_cluster_size_df_1), np.mean(largest_cluster_size_df_2), np.mean(largest_cluster_size_df_3)]

confronta_largest_cluster_size_serie.describe()

plt.figure(figsize = (10, 5))
plt.bar(['λ=λc', 'λ>λc', 'λ<λc'], confronta_largest_cluster_size_array, color = 'maroon')
plt.title('Largest Cluster Size Mean Comparison')
plt.xlabel('Lambda')
plt.ylabel('Largest Cluster Size Mean')

plt.show()

confronta_number_of_clusters_series = pd.concat([pd.Series(number_of_clusters_df_1, name = 'number_of_clusters_λ=λc'), pd.Series(number_of_clusters_df_2, name = 'number_of_clusters_λ>λc'), pd.Series(number_of_clusters_df_3, name = 'number_of clusters_λ<λc'), ], axis = 1)
confronta_number_of_clusters_array = [np.mean(number_of_clusters_df_1), np.mean(number_of_clusters_df_2), np.mean(number_of_clusters_df_3)]

confronta_number_of_clusters_series.describe()

plt.figure(figsize = (10, 5))
plt.bar(['λ=λc', 'λ>λc', 'λ<λc'], confronta_number_of_clusters_array, color = 'forestgreen')
plt.title('Number of Clusters Mean Comparison')
plt.xlabel('Lambda')
plt.ylabel('Number of Clusters Mean')

plt.show()

