import recordlinkage as rl
from IOoperation import load_people_record, write_result,load_people_record_test,write_pair,get_result_list
import time
import os

print("Load File Begins...")
load_start_time = time.clock()
#dfA = load_people_record_test()
dfA = load_people_record()
load_end_time = time.clock()
print("Load File Costs:%f s" % (load_end_time-load_start_time))

# Blocking
print("Blocking Begins...")
pcl = rl.SortedNeighbourhoodIndex(on=['EmplyeeID'], window=3)
pairs = pcl.index(dfA)
blocking_end_time = time.clock()
print("Blocking Costs:%f s" % (blocking_end_time-load_end_time))

# Comparison

print("Comparison Begins...")
compare_helper = rl.Compare()

# SSN length is 9 allowing miss 1 bit
compare_helper.string('SSN', 'SSN', threshold=0.85, label='SSN')
#compare_helper.string('EmplyeeID', 'EmplyeeID', threshold=0.85, label='EmplyeeID')
compare_helper.string('FNAME', 'FNAME', method='jarowinkler', threshold=0.85, label='FNAME')
compare_helper.string('LNAME', 'LNAME', method='jarowinkler', threshold=0.85, label='LNAME')
compare_helper.exact('MINIT', 'MINIT', label='MINIT')
compare_helper.string('CITY', 'CITY', threshold=0.85, label='CITY')
compare_helper.exact('STATE', 'STATE', label='STATE')
compare_helper.string('ZIP', 'ZIP', threshold=0.6, label='ZIP')
features = compare_helper.compute(pairs, dfA)

pair_match_end_time = time.clock()

print("Pairwise  Matching Cost:%f s" % (pair_match_end_time-blocking_end_time))
print(features)

# Cluster K-means
print("Cluster Begins...")
kmeans = rl.KMeansClassifier()
result_kmeans = kmeans.learn(features)

cluster_end_time = time.clock()
print("Cluster Cost:%f s" % (cluster_end_time-pair_match_end_time))

# res list like [[1,4,7],[0,5,9]] means 4 similar 5 and 1 simalar 0
res = []
for label in result_kmeans.labels:
    temp = []
    for item in label:
        temp.append(item.T)
    res.append(temp)

# ID process
cluster_list = []
# cluster_list like [[1,0],[4,5],[7,9]]
parent_dict = dict()
for i in range(len(res[0])):
    pair_id = []
    pair_id.append(int(res[0][i].T))
    pair_id.append(int(res[1][i].T))
    cluster_list.append(pair_id)
# print cluster_list
class_list = get_result_list(cluster_list)
write_result("di2017213857", class_list)
# write_result("result_test.csv", class_list)

# write_pair("result_pair.csv", cluster_list)



