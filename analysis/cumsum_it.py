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
        l = l.split(",")
        try:
            l = l[2].split(":")
            if l[0] == " train_acc":
                async_data.append(float(l[1]))
        except:
            continue


lines = file2.readlines()

for l in lines:
    if l:
        l = l.split(",")
        try:
            l = l[2].split(":")
            if l[0] == " train_acc":
                sync_data.append(float(l[1]))
        except:
            continue         

x = np.array(range(0,70))*10

y1 = np.array(async_data)[:70]
y2 = np.array(sync_data)[:70]

plt.fill_between(x, y1, y2, color='skyblue', alpha=0.5)
plt.plot(x, y1, zorder=1, label="Serene", alpha=0.7)
plt.plot(x, y2, zorder=1, label="Baseline", alpha=0.7)


#plt.scatter(y1, y2, s=x, color='blue', alpha=0.5)
#plt.plot(y1, y1, color='red', linestyle='--')  # Plot the line of equality


difference = np.array(async_data)[:70] - np.array(sync_data)[:70]
#plt.axis('equal')  # Ensure aspect ratio is equal

#residuals = np.abs(difference)

plt.plot(x, difference, zorder=1, label="Difference")

#plt.plot(residuals, zorder=1, label="Sync.")


plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)

plt.grid(zorder=-2, linestyle='--')
 
plt.xlabel("Training steps", fontsize = 16)
plt.ylabel("Training Accuracy", fontsize = 16)
#plt.title("Students enrolled in different courses")

plt.subplots_adjust(left=0.189, bottom=0.19, right=0.935, top=0.88, wspace=0.2, hspace=0.2)
plt.legend(loc ="center right",fontsize=14)

#sns.boxplot(sync_data, cumulative = True, color ='red', zorder=1)


plt.savefig("it_cumsum.pdf")
plt.show()