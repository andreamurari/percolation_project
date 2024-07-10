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
st.title("Percolation on Boolean Networks")
#FUNZIONI

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
with st.expander('Introduction'):
  """Percolation theory describes how the size of clusters of connected set of edges of large random networks
varies as the connectivity - i.e. the probability that two vertices are connected by an edge - changes. As the
connectivity increases the system undergoes a transition from a situation where the clusters are small in size to
a picture with significantly larger clusters. This transition is not smooth, but rather it happens sharply as the
connectivity crosses a critical value, called percolation threshold. 
The scope of the present project is to study numerically this phenomenon in Boolean networks.

\nWHAT IS A BOOLEAN NETWORK?

\nConsider X a Poisson process of density λ > 0 on the plane and take r > 0. A Boolean random
network on the plane, denoted by (X, λ, r), is constructed as follows: given a realization of the
Poisson process X, two elements x, y ∈ X are connected if their Euclidean distance is smaller than
or equal to 2r. This geometrically corresponds to placing discs of radius r at the points of the
Poisson process and considering connected components formed by clusters of overlapping discs.

\nGiven a random network, a cluster is a set of connected points and the cluster size is defined as the
number of nodes belonging to the cluster itself. Natural and relevant questions to address concern
the number of clusters present in the network and the size of the largest cluster.
The current project consists in what follows. Set r = 1 and taken a squared domain Λ = [0, T]×[0, T],
with T > 0 large, fixed a value of λ and made M independent simulations of the Boolean random
network (X, λ, 1), will be computed the empirical average of the M sizes of the largest cluster.
Then, by running several simulations and collecting the results in appropriate plots, will be investigated the following problems:"""
  """*  How the size of the largest cluster depends on λ, considering when it's > / < / = λc (=  4.512/4π)."""
  """*  How the number of clusters depends on λ."""
  
with st.expander('Analysis with λ free'):
  """
  In this section, fixed a value for "λ", are computed: the average size of the largest cluster, the average number of clusters and the average number of pointS. 
  \n The proposed values for the parameters T, λ, M are : 

  * T = 20 (MAX DOMAIN)
  * λ = 1 (LAMBDA)
  * M = 50 (NUMBER OF ITERATIONS)
  
  \nThese values can be changed with the checkbox below.
  """
    
  T = 20 #MAX DOMINIO
  l = 1 #LAMBDA
  M = 50 #NUMERO ITERAZIONI

  col_0, col_1 = st.columns([0.3, 0.7])
  with col_1:
    if st.checkbox('Modify values'):
      T = int(st.text_input('Insert " T " max dimension of the domain (max suggested = 40): ', 20))
      l = float(st.text_input('Insert value of  λ (max suggested = 2): ', 1))
      M = int(st.text_input('Insert number of iterations M: ', 50))

  with col_0:
    if st.checkbox('Use default values'):
      T = 20 #MAX DOMINIO
      l = 1 #LAMBDA
      M = 50 #NUMERO ITERAZIONI
      
  """Once the parameters are selected click the "Start Iterations" button below."""
  
  #ITERAZIONI E CREAZIONE DFs
  if st.button('Start Iterations'):
    with st.spinner('Executing iterations'):
      largest_cluster_size_df_0 = []
      number_of_clusters_df_0 = []
      number_of_ponits_df_0 = []
      for i in range(M):
        coordinates_x, coordinates_y, N = generate_poisson_coordinates(T, l)
        clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
        clusters = remove_duplicates(clusters_with_duplicates)
        clusters_with_duplicates = clusterizza_dbscan(coordinates_x, coordinates_y)
        clusters = remove_duplicates(clusters_with_duplicates)
        #st.write ('Iteration: ', i+1, '\nNumber of points: ', N, '\nNumber of clusters: ',  number_of_clusters(clusters), '\nLargest cluster size: ', largest_cluster_size(clusters), '\n')
        largest_cluster_size_df_0.append(largest_cluster_size(clusters))
        number_of_clusters_df_0.append(number_of_clusters(clusters))
        number_of_ponits_df_0.append(N)

      """Here can be seen the bar chart of:"""
      
      """* Number Of Points"""
      """*  Largest Cluster Size"""
      """*  Number of Clusters"""
              
      col_2, col_3, col_4 = st.columns(3)
      
      fig_01, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_ponits_df_0, color = 'cadetblue')
      plt.title('Number Of Points')
      plt.xlabel('Iteration')
      plt.ylabel('Number Of Points')
      plt.show()

      with col_2:
        st.pyplot(fig_01)

      fig_02, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), largest_cluster_size_df_0, color = 'maroon')
      plt.title('Largest Cluster Size')
      plt.xlabel('Iteration')
      plt.ylabel('Largest Cluster Size')
      plt.show()
      with col_3:
        st.pyplot(fig_02)

      fig_03, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_clusters_df_0, color = 'forestgreen')
      plt.title('Number of Clusters')
      plt.xlabel('Iteration')
      plt.ylabel('Number of Clusters')
      plt.show()
      with col_4:
        st.pyplot(fig_03)

      clusters_info_0 = pd.Series(largest_cluster_size_df_0, name = 'largest_cluster_size')
      clusters_info_0 = pd.concat([pd.Series(number_of_ponits_df_0, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_0, name = 'number_of_clusters'), clusters_info_0], axis = 1)

      mean_largest_cluster_size_0 = np.mean(largest_cluster_size_df_0)
      mean_number_of_clusters_0 = np.mean(number_of_clusters_df_0)
      st.write("As we can see from the following table, the mean of the largest cluster's size in ", M, "iterations is ", mean_largest_cluster_size_0, 
                "\n, the mean of the number of clusters is: ", mean_number_of_clusters_0,
                "and the average number of points is: ", np.mean(number_of_ponits_df_0))
      col_8, col_9, col_10 = st.columns([0.33, 0.34, 0.33])
      with col_9:
        st.write(clusters_info_0.describe())


      # Create a list to store colors for each cluster
      cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

      # Create a scatter plot with points colored by cluster
      fig_04, ax = plt.subplots(figsize = (5, 5))
      for i, cluster in enumerate(clusters):
        x_values = [coordinates_x[index] for index in cluster]
        y_values = [coordinates_y[index] for index in cluster]
        plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)], linewidths=100/T)
      plt.xticks(range(0, T + 1, int(T/10)))
      plt.yticks(range(0, T + 1, int(T/10)))
      plt.title('Scatter-plot of the last iteration')
      plt.show()
      """Finally, we can take a look at the scatter-plot of the last iteration: clusters are identified with different colors (some colors may be repeated)"""
      col_5, col_6, col_7 = st.columns([0.35, 0.3, 0.35])
      with col_6:
        st.pyplot(fig_04)


with st.expander('Analysis with λ = 4.512/4π'):
  """
  The parameters set for this section are:"""
  """
  * T = 20 (MAX DOMAIN)
  * λ = 4.512/(4*π) (LAMBDA)
  * M = 200 (NUMBER OF ITERATIONS)
  """

  T = 20 #MAX DOMINIO
  l = 4.512/(4*math.pi) #LAMBDA
  M = 200 #NUMERO ITERAZIONI
  """The values of T and M can be modified selecting the following checkbox, otherwise will be used the default parameters."""
  if st.checkbox('Modify values of T and M'):
      T = int(st.text_input('Insert " T " max dimension of the domain (max suggested = 40): ', 20))
      M = int(st.text_input('Insert number of iterations M: ', 200))
  
  """Once the parameters are selected click the "Start Iterations" button below."""
  
  #ITERAZIONI E CREAZIONE DFs
  if st.button('Start Iterations with λ = 4.512/4π'):
    with st.spinner('Executing iterations'):
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

      """Here can be seen the bar chart of:"""
      
      """* Number Of Points"""
      """*  Largest Cluster Size"""
      """*  Number of Clusters"""
      
      col_11, col_12, col_13 = st.columns(3)
      
      fig_11, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_ponits_df_1, color = 'cadetblue')
      plt.title('Number Of Points')
      plt.xlabel('Iteration')
      plt.ylabel('Number Of Points')
      plt.show()
      
      with col_11:
        st.pyplot(fig_11)
        
      fig_12, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), largest_cluster_size_df_1, color = 'maroon')
      plt.title('Largest Cluster Size')
      plt.xlabel('Iteration')
      plt.ylabel('Largest Cluster Size')
      plt.show()
      
      with col_12:
        st.pyplot(fig_12)
        
      fig_13, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_clusters_df_1, color = 'forestgreen')
      plt.title('Number of Clusters')
      plt.xlabel('Iteration')
      plt.ylabel('Number of Clusters')
      plt.show()

      with col_13:
        st.pyplot(fig_13)
          
          
      clusters_info_1 = pd.Series(largest_cluster_size_df_1, name = 'largest_cluster_size')
      clusters_info_1 = pd.concat([pd.Series(number_of_ponits_df_1, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_1, name = 'number_of_clusters'), clusters_info_1], axis = 1)

      mean_largest_cluster_size_1 = np.mean(largest_cluster_size_df_1)
      mean_number_of_clusters_1 = np.mean(number_of_clusters_df_1)
      st.write("As we can see from the following table, the mean of the largest cluster's size in ", M, "iterations is ", mean_largest_cluster_size_1, 
                "\n, the mean of the number of clusters is: ", mean_number_of_clusters_1,
                "and the average number of points is: ", np.mean(number_of_ponits_df_1))
      col_14, col_15, col_16 = st.columns([0.33, 0.34, 0.33])
      with col_15:
        st.write(clusters_info_1.describe())
      
      # Create a list to store colors for each cluster
      cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

      # Create a scatter plot with points colored by cluster
      fig_14, ax = plt.subplots(figsize = (5, 5))
      for i, cluster in enumerate(clusters):
        x_values = [coordinates_x[index] for index in cluster]
        y_values = [coordinates_y[index] for index in cluster]
        plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)], linewidths=100/T)
      plt.xticks(range(0, T + 1, int(T/10)))
      plt.yticks(range(0, T + 1, int(T/10)))
      plt.title('Scatter-plot of the last iteration')
      plt.show()
      
      """Finally, we can take a look at the scatter-plot of the last iteration: clusters are identified with different colors (some colors may be repeated)"""
      col_17, col_18, col_19 = st.columns([0.35, 0.3, 0.35])
      with col_18:
        st.pyplot(fig_14)


with st.expander('Analysis with λ > 4.512/4π'):
  
  """
  The default parameters set for this section are:"""
  """
  * T = 20 (MAX DOMAIN)
  * λ > 4.512/(4*π) (LAMBDA)
  * M = 200 (NUMBER OF ITERATIONS)
  """
  T = 20 #MAX DOMINIO
  l = 4.512/(2*math.pi) #LAMBDA
  M = 200 #NUMERO ITERAZIONI

  """The values of T, λ and M can be modified selecting the following checkbox, otherwise will be used the default parameters. 
  \nWARNING: T and M of thi section must be the same of the previous section and λ > 4.512/4π"""
  if st.checkbox('Modify values for λ > 4.512/4π'):
      T = int(st.text_input('Insert " T " max dimension of the domain (max suggested = 40): ', 20))
      l = float(st.text_input('Insert value of  λ (max suggested = 2): ', 4.512/(2*math.pi)))
      M = int(st.text_input('Insert number of iterations M: ', 200))
  
  """Once the parameters are selected click the "Start Iterations" button below."""
  
  #ITERAZIONI E CREAZIONE DFs
  if st.button('Start Iterations with λ > 4.512/4π'):
    with st.spinner('Executing iterations'):
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
      
      """Here can be seen the bar chart of:"""
      
      """* Number Of Points"""
      """*  Largest Cluster Size"""
      """*  Number of Clusters"""
      
      col_20, col_21, col_22 = st.columns(3)
      
      fig_21, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_ponits_df_2, color = 'cadetblue')
      plt.title('Number Of Points')
      plt.xlabel('Iteration')
      plt.ylabel('Number Of Points')
      plt.show()

      with col_20:
        st.pyplot(fig_21)
        
      fig_22, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), largest_cluster_size_df_2, color = 'maroon')
      plt.title('Largest Cluster Size')
      plt.xlabel('Iteration')
      plt.ylabel('Largest Cluster Size')
      plt.show()
      
      with col_21:
        st.pyplot(fig_22)

      fig_23, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_clusters_df_2, color = 'forestgreen')
      plt.title('Number of Clusters')
      plt.xlabel('Iteration')
      plt.ylabel('Number of Clusters')
      plt.show()

      with col_22:
        st.pyplot(fig_23)
      
      clusters_info_2 = pd.Series(largest_cluster_size_df_2, name = 'largest_cluster_size')
      clusters_info_2 = pd.concat([pd.Series(number_of_ponits_df_2, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_2, name = 'number_of_clusters'), clusters_info_2], axis = 1)

      mean_largest_cluster_size_2 = np.mean(largest_cluster_size_df_2)
      mean_number_of_clusters_2 = np.mean(number_of_clusters_df_2)
      st.write("As we can see from the following table, the mean of the largest cluster's size in ", M, "iterations is ", mean_largest_cluster_size_2, 
                "\n, the mean of the number of clusters is: ", mean_number_of_clusters_2,
                "and the average number of points is: ", np.mean(number_of_ponits_df_2))
      col_23, col_24, col_25 = st.columns([0.33, 0.34, 0.33])
      
      with col_24:
        st.write(clusters_info_2.describe())

      # Create a list to store colors for each cluster
      cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

      # Create a scatter plot with points colored by cluster
      fig_24, ax = plt.subplots(figsize = (5, 5))
      for i, cluster in enumerate(clusters):
        x_values = [coordinates_x[index] for index in cluster]
        y_values = [coordinates_y[index] for index in cluster]
        plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)], linewidths=100/T)
      plt.xticks(range(0, T + 1, int(T/10)))
      plt.yticks(range(0, T + 1, int(T/10)))
      plt.title('Scatter-plot of the last iteration')
      plt.show()
      
      """Finally, we can take a look at the scatter-plot of the last iteration: clusters are identified with different colors (some colors may be repeated)"""
      col_26, col_27, col_28 = st.columns([0.35, 0.3, 0.35])
      with col_27:
        st.pyplot(fig_24)


with st.expander('Analysis with λ < 4.512/4π'):
  """
  The default parameters set for this section are:"""
  """
  * T = 20 (MAX DOMAIN)
  * λ < 4.512/(4*π) (LAMBDA)
  * M = 200 (NUMBER OF ITERATIONS)
  """
  T = 20 #MAX DOMINIO
  l = 4.512/(8*math.pi) #LAMBDA
  M = 200 #NUMERO ITERAZIONI

  """The values of T, λ and M can be modified selecting the following checkbox, otherwise will be used the default parameters. 
  \nWARNING: T and M of thi section must be the same of the previous section and λ > 4.512/4π"""
  if st.checkbox('Modify values for λ < 4.512/4π'):
      T = int(st.text_input('Insert " T " max dimension of the domain (max suggested = 40): ', 20))
      l = float(st.text_input('Insert value of  λ (max suggested = 2): ', round(4.512/(8*math.pi), 3)))
      M = int(st.text_input('Insert number of iterations M: ', 200))
  
  """Once the parameters are selected click the "Start Iterations" button below."""
  
  #ITERAZIONI E CREAZIONE DFs
  if st.button('Start Iterations with λ < 4.512/4π'):
    with st.spinner('Executing iterations'):
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
        
      """Here can be seen the bar chart of:"""
      
      """* Number Of Points"""
      """*  Largest Cluster Size"""
      """*  Number of Clusters"""
      
      col_29, col_30, col_31 = st.columns(3)
      
      fig_31, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_ponits_df_3, color = 'cadetblue')
      plt.title('Number Of Points')
      plt.xlabel('Iteration')
      plt.ylabel('Number Of Points')
      plt.show()
      
      with col_29:
        st.pyplot(fig_31)

      fig_32, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), largest_cluster_size_df_3, color = 'maroon')
      plt.title('Largest Cluster Size')
      plt.xlabel('Iteration')
      plt.ylabel('Largest Cluster Size')
      plt.show()
      
      with col_30:
        st.pyplot(fig_32)
      
      fig_33, ax = plt.subplots(figsize = (10,5))
      plt.bar(range(M), number_of_clusters_df_3, color = 'forestgreen')
      plt.title('Number of Clusters')
      plt.xlabel('Iteration')
      plt.ylabel('Number of Clusters')
      plt.show()

      with col_31:
        st.pyplot(fig_33)

      clusters_info_3 = pd.Series(largest_cluster_size_df_3, name = 'largest_cluster_size')
      clusters_info_3 = pd.concat([pd.Series(number_of_ponits_df_3, name = 'number_of_ponits'), pd.Series(number_of_clusters_df_3, name = 'number_of_clusters'), clusters_info_3], axis = 1)

      mean_largest_cluster_size_3 = np.mean(largest_cluster_size_df_3)
      mean_number_of_clusters_3 = np.mean(number_of_clusters_df_3)
      st.write("As we can see from the following table, the mean of the largest cluster's size in ", M, "iterations is ", mean_largest_cluster_size_3, 
                "\n, the mean of the number of clusters is: ", mean_number_of_clusters_3,
                "and the average number of points is: ", np.mean(number_of_ponits_df_3))
      col_32, col_33, col_34 = st.columns([0.33, 0.34, 0.33])
      
      with col_33:
        st.write(clusters_info_3.describe())


      # Create a list to store colors for each cluster
      cluster_colors = ['cyan', 'magenta', 'lightgreen', 'skyblue', 'pink']

      # Create a scatter plot with points colored by cluster
      fig_34, ax = plt.subplots(figsize = (5, 5))
      for i, cluster in enumerate(clusters):
        x_values = [coordinates_x[index] for index in cluster]
        y_values = [coordinates_y[index] for index in cluster]
        plt.scatter(x_values, y_values, c=cluster_colors[i % len(cluster_colors)], linewidths=100/T)
      plt.xticks(range(0, T + 1, int(T/10)))
      plt.yticks(range(0, T + 1, int(T/10)))
      plt.title('Scatter-plot of the last iteration')
      plt.show()

      """Finally, we can take a look at the scatter-plot of the last iteration: clusters are identified with different colors (some colors may be repeated)"""
      col_35, col_36, col_37 = st.columns([0.35, 0.3, 0.35])
      with col_36:
        st.pyplot(fig_34)

with st.expander('Final comparison'):
  """###CONFRONTO"""
  if st.button('Elaborate final comparison'):
    with st.spinner('Executing iterations'):
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

