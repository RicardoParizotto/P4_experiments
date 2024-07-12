# defining the libraries 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

plt.rcParams['font.family'] = 'sans-serif'


fig,ax = plt.subplots(figsize=(6, 4))


file1 = open("../testbed/aggregation/server2_gpu6/agents/example1/h1.log", "r")
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
        
plt.plot(np.array(async_data)[:700].cumsum(), zorder=1, label="Serene")
plt.plot(np.array(sync_data)[:700].cumsum(), zorder=1, label="Baseline")


plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)

plt.grid(zorder=-2, linestyle='--')
 
plt.xlabel("Training steps", fontsize = 16)
plt.ylabel("Cumulative Waiting Time (s)", fontsize = 16)
#plt.title("Students enrolled in different courses")

plt.subplots_adjust(left=0.189, bottom=0.19, right=0.935, top=0.88, wspace=0.2, hspace=0.2)
plt.legend(loc ="upper left",fontsize=14)

#sns.boxplot(sync_data, cumulative = True, color ='red', zorder=1)


plt.savefig("wt_cumsum.pdf")
plt.show()