import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('alert_part1.csv')

kmeans = KMeans(n_clusters=6).fit(df) #we are using 6 clusters

centroids = kmeans.cluster_centers_

print(centroids) #lists all 6 centroid coordinates
