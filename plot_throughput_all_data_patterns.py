import sys
import matplotlib.pyplot as plt
import subprocess
from plotters_all_data_patterns import plot_bars
import numpy as np

names = ["ac-snort", \
         "dfc-cpu", \
         "pfac", \
         "dfc", \
         "dfc_vec", \
         "combined", \
         "combined_vec"]

fancy_names = ["AC (CPU)", \
         "DFC (CPU)", \
         "PFAC", \
         "DFC", \
         "DFC vect", \
         "COMB", \
         "COMB vect"] 

need_correction = [ "ac-snort", "dfc-cpu"]

datasets = ["outside_http.pcap", "testbed_payload_small", "bigFlows.pcap_small","random.data_small"]
fancy_dataset_names = [" DARPA", "ISCX", "BigFlows", "Random"]
patterns = ["http_related_rules","emerging_all_5000"]

def get_versions(D, pat, dat, metric):
    l = []
    for n in names:
        l.append(D[n,pat,dat][metric])
    return l

def get_datasets(D, pat, version, metric):
    l = []
    for d in datasets:
        l.append(D[version,pat,d][metric])
    return l

Data = {}

for v in names:
    with open("logs/"+v+"_throughput.log",'rb') as log:
        for row in log:
            dev_write = 0 
            dev_read = 0
            post_proc = 0
            file_read = 0
            v = row.split("version: ")[1].split()[0]
            pat = row.split("patterns: ")[1].split()[0].split('/')[-1]
            dataset = row.split("dataset: ")[1].split()[0].split('/')[-1]
            kernel_exec = float(row.split("kernel_exec: ")[1].split()[0])
            if "dev_write" in row:
                dev_write = float(row.split("dev_write: ")[1].split()[0])
            if "dev_read" in row:
                dev_read = float(row.split("dev_read: ")[1].split()[0])
            if "post_proc" in row:
                post_proc = float(row.split("post_proc: ")[1].split()[0])
            if "file_read" in row:
                file_read = float(row.split("file_read: ")[1].split()[0])
            
            if not Data.has_key((v,pat,dataset)):
                Data[(v,pat,dataset)] = {"kernel_exec": [kernel_exec], "dev_write": [dev_write], \
                        "dev_read": [dev_read], "post_proc": [post_proc], "file_read": [file_read]}
            else:
                Data[(v,pat,dataset)]["kernel_exec"].append(kernel_exec)
                Data[(v,pat,dataset)]["dev_write"].append(dev_write)
                Data[(v,pat,dataset)]["dev_read"].append(dev_read)
                Data[(v,pat,dataset)]["post_proc"].append(post_proc)
                Data[(v,pat,dataset)]["file_read"].append(file_read)

SD={}
### average the runs ###
for x in Data:
    SD[x]={}
    if x[0] in need_correction:
        Data[x]["kernel_exec"] = list( np.array(Data[x]["kernel_exec"]) -  np.array(Data[x]["file_read"]))

    s = 0
    for y in Data[x]:
        SD[x][y] =  np.std(Data[x][y])
        Data[x][y] = sum(Data[x][y])/float(len(Data[x][y]))
        s += Data[x][y]
    Data[x]["sum"] = s
    


kernels = [get_datasets(Data,patterns[0],names[0],"sum")] 
kernels.append(get_datasets(Data,patterns[0],names[1],"sum"))
kernels.append(get_datasets(Data,patterns[0],names[2],"sum"))
kernels.append(get_datasets(Data,patterns[0],names[3],"sum"))
kernels.append(get_datasets(Data,patterns[0],names[4],"sum"))
kernels.append(get_datasets(Data,patterns[0],names[5],"sum"))
kernels.append(get_datasets(Data,patterns[0],names[6],"sum"))


stdz = [[0]*len(kernels[0])] * len(kernels)

print kernels, stdz
FIG_SIZE=(20,10)
fig , ax = plt.subplots(1,1,figsize=FIG_SIZE)
legend = fancy_names
lgd = plot_bars(ax,kernels,fancy_dataset_names,"Data sets", legend, [], stdz, show_legend=True, on_top=False)
ax.set_ylim(0, 3600)

name="/home/odroid/chasty-dfc-benchmarks/plots/all_datasets_http_rules.pdf"
plt.savefig(name,bbox_extra_artists=(lgd,), bbox_inches = "tight")
subprocess.Popen("pdfcrop "+name+" "+name,shell=True)
subprocess.Popen("pdfcrop")

plt.show()

