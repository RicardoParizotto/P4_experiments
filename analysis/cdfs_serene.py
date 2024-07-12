# defining the libraries 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

plt.rcParams['font.family'] = 'sans-serif'


fig,ax = plt.subplots(figsize=(6, 3))


file1 = open("../testbed/aggregation/server1_tb1/agents/example1/async_straggler/h0.log", "r")
file2 = open("../testbed/aggregation/server2_gpu6/agents/example1/sync_straggler/h1.log", "r")
async_data = []
sync_data = []

lines = file1.readlines()

for l in lines:
    if l:
        l = l.split(":")
        if l[0] == "#waiting":
            async_data.append(float(l[1]))


lines = file2.readlines()

for l in lines:
    if l:
        l = l.split(":")
        if l[0] == "#waiting":
            sync_data.append(float(l[1]))            
        
#sns.barplot([np.percentile(np.array(async_data)[:150], 90), np.percentile(np.array(sync_data)[:150], 90)], zorder=1)
sns.kdeplot(sync_data[:150], cumulative = True, color ='red', zorder=1)
sns.kdeplot(async_data[:150], cumulative = True, color ='red', zorder=1)



plt.savefig("serene.pdf")
plt.show()