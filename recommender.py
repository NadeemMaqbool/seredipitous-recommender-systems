import statistics
import sys
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pytz as tz
import matplotlib.pyplot as plt
import csv

from statistics import mean
from collections import defaultdict

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

user_recomm = defaultdict(list)
# df = pd.read_csv('gowalla_.txt', header =None)

def write_in_file(outputfile1, u, line):
    with open(outputfile1, 'a+') as f:
        f.write(str(u) + "\t")
        for i in line:
            f.write(str(i) + ",")
        f.write("\n")
        
def recommender(file, outputfile):
    df = open(file,"r").readlines()
    user_sim = {}
    df_list = {}
    pair = {}
    userlist = set()
    for line in df:
        user, locid, freq  = line.strip().split()
        user, locid, freq = int(user), int(locid) , int(freq)
        userlist.add(user)
        df_list[user, locid] = (freq)

    total_users = len(userlist)
    sum = 0
    count = 0
    y_data = {}
    
    for j in df_list:
        y_data[j] = [df_list[j], 0]


    for i in (userlist):
        for j in df_list:
            if (i == j[0]):      
                sum = sum + df_list[j]
                count +=1
        avg = sum/count
        for k in df_list:
            if (i == k[0]): 
                if df_list[k] > avg:
                    y_data[k][1] = 1


    locations = defaultdict(int)
    for i in df_list:
        locations[i[1]] += 1

    # ========================================================================================
    popularity = []
    unexpectedness = []

    for x in locations:
        loc_pop = locations[x]/total_users
        locations[x] = (locations[x],) + (loc_pop,)
        popularity.append(loc_pop)    

    avg_popularity = mean(popularity)

    for j in locations:
        x = list(locations[j])
        if locations[j][1] > avg_popularity:
            x.append(1)
            locations[j] = (x)
            unexpectedness.append(1)

        else:
            x.append(0)
            locations[j] = (x)
            unexpectedness.append(0)

    avg_unexpectedness = mean(unexpectedness)
    
    
    for y in y_data:
        for a in locations:
            if (a == y[1]):
                 y_data[y].append(locations[a][2])

    for y in y_data:
        if (y_data[y][1] == 1 and y_data[y][2] == 1):
             y_data[y].append(1)
        else:
            y_data[y].append(0)
        
    combined_sim_loc = []
    superarray = []

    for i in range(0, total_users):

        counts_recom = 0
        ruser_compare = {}
        locer_compare = []
        ruser = {}
        locer = []
        lister = []
        array = []
        for j in df_list:
            if (i == j[0]):
                ruser[j] = df_list[j]
                locer.append(j[1])

        for n in range(0, total_users):
            count = 0
            if (i == n):
                continue

            else:
                for m in df_list:
                    if (n == m[0]):
                        ruser_compare[m] = df_list[m]
                        locer_compare.append(m[1])

                for j in locer:
                    for k in locer_compare:
                        if (j == k):
                            count += 1
                        else:
                            if k not in locer:
                                array.append(k)
                        
#                         if (count <= 5):
#                             if (j == k):
#                                 count += 1
#                             else:
#                                 if k not in locer:
#                                     array.append(k)
#                         else:
#                             break

                if (count >= 5):
                    lister.append(n)
                
        for lc in lister:
            
            for lis in set(array):
                for y in y_data:       
                    if (lc == y[0]):
                        if (y[1] == lis) and ((y_data[y][3]) == 1):
                            if ((y[1] not in user_recomm[i])):

                                user_recomm[i].append(y[1])
                                counts_recom +=1
                                
                                    
        write_in_file(outputfile, i, user_recomm[i])
        print("writing....")
    #         if lister != []:

file = open("recommended_locations.txt","w")
file.close()

recommender("gowalla_100.txt","recommended_locations.txt")
file.close()

user_recomm = defaultdict(list)
# df = pd.read_csv('gowalla_.txt', header =None)

#df_test = open("recommended_locations_test.txt","r").readlines()
df_test = open("recommended_locations_test.txt","r").readlines()
#df_test = open("Gowalla_test.txt","r").readlines()
dftest_list = {}
locationtest = defaultdict(list)
usertestlist = set()
for line in df_test:
    usertest, loctest = line.split("\t")
    loctest = loctest.split(',')
    
    recloc_cleaner = loctest.pop()
    loctest = [int(r) for r in loctest]
    
    locationtest[usertest].append(loctest)
    
index = 0
loc_s = 0
precision=0
recall=0
fmeas=0
for temp in range(5, 21, 5):
    index = 0
    prec_all = 0
    recal_all = 0
    fmeas_all = 0
    for line in output:
        if (line != ''):
            uid, recloc = line.split("\t")
            recloc = recloc.split(',')
            recloc_cleaner = recloc.pop()
            recloc = [int(r) for r in recloc] 
            index += 1
            length = len(recloc)
            loc_s = recloc[:temp]
            
            for i in loc_s:  
                relevance_count = 0
                
                for j in locationtest:
                    
                   
                    if(int(j) == int(uid)):        
                        location_temp = locationtest[j][0]
                        for k in location_temp:
                            
                            if k in loc_s:
                                relevance_count += 1
                        
                        fmeas = 0            
                        precision = relevance_count/temp
                        
                        if(len(locationtest[uid][0]) > 0):
                            recall = relevance_count/len(locationtest[uid][0])
                        else:
                            recall = 0
                        if(precision > 0 and recall> 0):
                            fmeas = (2 * precision * recall) / (precision + recall)

            prec_all = prec_all + precision
            recal_all = recal_all + recall
            fmeas_all = fmeas_all + fmeas

            print(index, uid, "precison: @" + str(temp), precision, "recall: @" + str(temp), recall, "F-measure: @" + str(temp), fmeas)

    print("--------------------------------------------------------------------------------------------------")
    print("Avg precison:",prec_all/index, "Avg recall:", recal_all/index, "Avg F-measure:", fmeas_all/index)
    print("--------------------------------------------------------------------------------------------------")