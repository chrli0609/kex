import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#plots the k-means elbow graph for the alert code data

df = pd.read_csv('alert_part1.csv')

limit = int((df.shape[0] // 2) ** 0.5)

wcss = {}
c
for k in range(2, limit + 1):
    model = KMeans(n_clusters=k)
    model.fit(df)
    wcss[k] = model.inertia_

plt.plot(wcss.keys(), wcss.values(), 'gs-')
plt.xlabel('Values of "k"')
plt.ylabel('WCSS')
plt.show() #shows that optimal number of clusters is 6
