
PrevState = 'Continue'
off2offCounter = 0
off2onCounter = 0
on2offCounter = 0
on2onCounter = 0
onPrevCounter = 0
offPrevCounter = 0

with open('state_part1.csv') as openfileobject:
    for line in openfileobject:
        rowStr = openfileobject.readline()
        rowArr = rowStr.split(',')
    
        for i in range(len(rowArr)):
            #Cannot compare first row (also is always continue so doesn't matter)
            if i > 0:
                if rowArr[i-1] == 'Continue':
                    offPrevCounter += 1
                    if rowArr[i] == 'Continue':
                        off2offCounter += 1
                    if rowArr[i] != 'Continue':
                        off2onCounter += 1
                elif rowArr[i-1] != 'Continue':
                    onPrevCounter += 1
                    if rowArr[i] == 'Continue':
                        on2offCounter += 1
                    if rowArr[i] != 'Continue':
                        on2onCounter += 1
                else:
                    print("An Error has occured in counter loop")
                
                    
openfileobject.close()

off2offProb = off2offCounter/offPrevCounter
off2onProb = off2onCounter/offPrevCounter
on2offProb = on2offCounter/onPrevCounter
on2onProb = on2onCounter/onPrevCounter

print("off2offProb: ", off2offProb)
print("off2onProb: ", off2onProb)
print("on2offProb: ", on2offProb)
print("on2onProb: ", on2onProb)



#Emission matrix

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

print("Centroids:\n", centroids) #lists all 6 centroid coordinates

kmeans.labels_


cluster_map = pd.DataFrame()
cluster_map['data_index'] = emi_df.index.values
cluster_map['cluster'] = kmeans.labels_

#Find max and min values in every cluster

#parameter: df, det cluster man vill undersöka
#returnerar en array där arr[0] = maxvärdet, arr[1] = minvärdet
def find_max_min(df, cluster):

    startMin = 1000000
    
    maxArr = []
    minArr = []
    currMax = 0
    currMin = startMin
    retArr = []

    #Sparar alla alert codes för den cluster i en array
    for i in range(len(cluster_map.axes[0])):
        clusterNum = cluster_map.loc[i].at['cluster']
        if clusterNum == cluster:
            maxArr.append(df.loc[i].at['Alert Code'])
            minArr.append(df.loc[i].at['Alert Code'])

    #Hitta max värdet i arrayen
    for j in range(len(maxArr)):
        if maxArr[j] > currMax:
            currMax = maxArr[j]

    #Hitta min värdet i array
    for k in range(len(minArr)):
        if minArr[k] < currMin:
            currMin = minArr[k]
    retArr.append(currMax)
    retArr.append(currMin)
    if len(retArr) != 2:
        print("An Error has occured in find_max_min, retArr assignment")
    if minArr == startMin:
        print("An Error has occured in find_max_min, minArr has not been assigned properly")
    return retArr



maxValArr = []
minValArr = []
print("_____________________________________")
print("Max and min values of clusters: ")

for i in range(6):
    tmpArr = find_max_min(emi_df,i)
    print("cluster ",i,"{ max: ", tmpArr[0], " min: ",tmpArr[1], " }")
    maxValArr.append(tmpArr[0])
    minValArr.append(tmpArr[1])




#Matcha in alla alert codes i olika clusters


#Returns a double array where (Emission matrix):
    #rows are clusters
    #columns are on/off intrusion (on is index 0)
    #the value is the probability that with the current observed cluster, what is the true state
    #ex. retArr[3][1] returns the probability that the real state is no intrusion when the observed cluster is cluster 4 (of 6 clusters)
def getEmission(alert_df, state_df, maxValArr, minValArr):
    #Create empty double array (to return)
    tmpArr = []
    retArr = []
    for row in range(6):
        tmpArr.append([])
        retArr.append([])
        for column in range(2):
            tmpArr[row].append(0)
            retArr[row].append(0)

    totState = [0, 0]
    #Går igenom alla alert codes
    for i in range(len(alert_df.axes[0])):
        for j in range(len(alert_df.axes[1])):
            alertCode = alert_df.loc[i].at[str(j)]
            #Kollar vilken cluster som den aler code tillhör
            for k in range(6):
                if alertCode >= minValArr[k] and alertCode <= maxValArr[k]:                    
                    state = state_df.loc[i].at[str(j)]
                    if state != 'Continue':
                        tmpArr[k][0] += 1
                        totState[0] += 1
                    elif state == 'Continue':
                        tmpArr[k][1] += 1
                        totState[1] += 1
                    else:
                        print("An Error has occurred in getEmission, retArr counter loop")

    #dividera med totala antalet gånger den clustern uppkommer i datat för att få sannolikheten (från absoluta mängden i förra delen)
    for h in range(6):
        for l in range(2):
            retArr[h][l] = tmpArr[h][l]/totState[l]
                    
    return retArr
                

emission_matrix = getEmission(df_1, df_2, maxValArr, minValArr)
print("_________________________________")
print("Emission Matrix: \n", emission_matrix)

