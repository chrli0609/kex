#Cluster data with sklearn

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

df_1 = pd.read_csv("alert_part1.csv") #skapar en dataframe från filen
df_2 = pd.read_csv("state_part1.csv")

#print(df_1)
#print(df_2)


newArr = []
alertArr = []
stateArr = []

for i in range(len(df_1.axes[0])):
    for j in range(len(df_1.axes[1])):
        if df_2.loc[i].at[str(j)] == 'Continue':
            newArr.append([df_1.loc[i].at[str(j)], 0])
            alertArr.append(df_1.loc[i].at[str(j)])
            stateArr.append(0)
        elif df_2.loc[i].at[str(j)] != 'Continue':
            newArr.append([df_1.loc[i].at[str(j)], 1])
            alertArr.append(df_1.loc[i].at[str(j)])
            stateArr.append(1)
        else:
            print("Error in Emission Loop")

emi_df = pd.DataFrame(newArr, columns = ["Alert Code", "Activity"])



kmeans = KMeans(n_clusters=6).fit(emi_df) #we are using 6 clusters

centroids = kmeans.cluster_centers_

print("Centroids: ", centroids) #lists all 6 centroid coordinates

kmeans.labels_


#PLOT Centroid points

import matplotlib.pyplot as plt

npNewArr = np.array(newArr)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(npNewArr[:,0], npNewArr[:,1],s=1, c = 'b', marker = "o", label='data')
ax.scatter(centroids[:,0], centroids[:,1], s=10, c = 'r', marker = "o", label='centroids')
plt.xlabel("Alert Code")
plt.ylabel("State")
plt.show()

cluster_map = pd.DataFrame()
cluster_map['data_index'] = emi_df.index.values
cluster_map['cluster'] = kmeans.labels_
