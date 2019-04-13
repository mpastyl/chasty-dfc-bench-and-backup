import sys
import matplotlib.pyplot as plt
import subprocess
from plotters import plot_bars
import numpy as np

names = ["ac-snort", \
         "dfc-cpu", \
         "pfac", \
         "dfc", \
         "dfc_vec", \
         "combined", \
         "combined_vec"]
fancy_names = [ \
            "AC\n(CPU)", \
            "DFC\n(CPU)", \
            "PFAC\n(GPU)", \
            "DFC\n(GPU)", \
            "DFC Vect\n(GPU)", \
            "HYBRID\n(GPU)", \
            "HYBRID\nVect (GPU)"]

need_correction = [ "ac-snort", "dfc-cpu"]

datasets = ["outside_http.pcap"]
patterns = ["http_related_rules"]

def get_versions(D, pat, dat, metric):
    l = []
    for n in names:
        l.append(D[n,pat,dat][metric])
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
    for y in Data[x]:
        SD[x][y] =  np.std(Data[x][y])
        Data[x][y] = sum(Data[x][y])/float(len(Data[x][y]))
    

print Data

kernels = [get_versions(Data,patterns[0],datasets[0],"file_read")] 
kernels.append(get_versions(Data,patterns[0],datasets[0],"dev_write"))
kernels.append(get_versions(Data,patterns[0],datasets[0],"kernel_exec")) 
kernels.append(get_versions(Data,patterns[0],datasets[0],"dev_read")) 
kernels.append(get_versions(Data,patterns[0],datasets[0],"post_proc")) 
stdz = [[0]*len(kernels[0])]*len(kernels)
#stdz = [get_versions(SD,patterns[0],datasets[0],"file_read")] 
#stdz.append(get_versions(SD,patterns[0],datasets[0],"dev_write"))
#stdz.append(get_versions(SD,patterns[0],datasets[0],"kernel_exec")) 
#stdz.append(get_versions(SD,patterns[0],datasets[0],"dev_read")) 
#stdz.append(get_versions(SD,patterns[0],datasets[0],"post_proc")) 


print kernels, stdz
FIG_SIZE=(6,2.5)
fig , ax = plt.subplots(1,1,figsize=FIG_SIZE)
#legend = ["read_from_file","write to dev","execution","read from dev","post_processing"]
legend = ["Read from file", "Write to device", "Pattern matching execution","Read from device","Post-procesing"]
lgd = plot_bars(ax,kernels,fancy_names,"Versions", legend, [], stdz, show_legend=True, on_top=True)
ax.set_ylim(0, 3600)
plt.autoscale(axis='x',tight=True)

name="/Users/mpastyl/clone_dfc_odroid_results/chasty-dfc-bench-and-backup/plots/execution_time_stacked.pdf"
plt.savefig(name,bbox_extra_artists=(lgd,), bbox_inches = "tight")
subprocess.Popen("pdfcrop "+name+" "+name,shell=True)
subprocess.Popen("pdfcrop")

plt.show()


print "Comparisons"
print " AC total / Hybrid total" , float( kernels[0][0] + kernels[2][0]) / (kernels[0][5] + kernels[1][5]+ kernels[2][5]+ kernels[3][5]+ kernels[4][5])
print " AC exec / Hybrid exec" ,  float(kernels[2][0]) / kernels[2][5]
print " DFC (GPU) / PFAC", float(kernels[2][3])/kernels[2][2]
print " PFAC exec / HYBRID exec", float(kernels[2][2])/kernels[2][5]
print " DFC (GPU) exec / HYBRID exec", float(kernels[2][3])/kernels[2][5]

for i,name in enumerate(fancy_names):
    print "--------------"
    print "name: ",name
    print "read from file: ", kernels[0][i]
    print "write to dev: ", kernels[1][i]
    print "Execute: ", kernels[2][i]
    print "Read from dev", kernels[3][i]
    print "Post proc", kernels[4][i]
    print "Total time:", kernels[0][i] + kernels[1][i] +kernels[2][i] +kernels[3][i]+ kernels[4][i]
    print "time impr: ", float(kernels[0][0] + kernels[1][0] +kernels[2][0] +kernels[3][0]+ kernels[4][0])/ (kernels[0][i] + kernels[1][i] +kernels[2][i] +kernels[3][i]+ kernels[4][i])
