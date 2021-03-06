import sys
import matplotlib.pyplot as plt
import subprocess
from plotters_energy import plot_bars
import numpy as np

fancy_names = [ \
            "AC\n(CPU)", \
            "DFC\n(CPU)", \
            "PFAC\n(GPU)", \
            "DFC\n(GPU)", \
            "DFC Vect\n(GPU)", \
            "HYBRID\n(GPU)", \
            "HYBRID\nVect (GPU)"\
			]


ac_en = "a15-watt    841.601 a17-watt     55.473 gpu-watt     47.336 mem-watt     20.583 Total_energy 964.993"

dfc_cpu_en = "a15-watt    913.411 a17-watt     55.706 gpu-watt     47.770 mem-watt     16.990 Total_energy 1033.877"

pfac_en = "a15-watt    322.534 a17-watt     52.246 gpu-watt    137.496 mem-watt     24.778 Total_energy 537.054"

dfc_en = "a15-watt    398.396 a17-watt     67.109 gpu-watt    205.917 mem-watt     34.317 Total_energy 705.739"

dfc_vec_en = "a15-watt   418.258 a17-watt     70.403 gpu-watt    230.247 mem-watt     47.228 Total_energy 766.136"

hybrid_en = "a15-watt    323.180 a17-watt     50.954 gpu-watt    110.878 mem-watt     20.988 Total_energy 506.0"

hybrid_vec_en = "a15-watt    341.908 a17-watt     52.612 gpu-watt    130.096 mem-watt     26.730 Total_energy 551.346"

ALL = [ac_en, dfc_cpu_en, pfac_en, dfc_en, dfc_vec_en, hybrid_en, hybrid_vec_en]

total_en = []
cpu_en = []
gpu_en = []
mem_en = []
for v in ALL:
    x = float(v.split("Total_energy ")[1])
    cpu = float(v.split()[1])
    gpu = float(v.split()[5])
    mem = float(v.split()[7])
    print cpu
    print gpu
    print mem
    total_en.append(x)
    cpu_en.append(cpu)
    gpu_en.append(gpu)
    mem_en.append(mem)


kernels = [cpu_en, gpu_en]
print kernels
stdz = [[0]*len(kernels[0])]*len(kernels)

FIG_SIZE=(6,2.5)
fig , ax = plt.subplots(1,1,figsize=FIG_SIZE)
#legend = ["read_from_file","write to dev","execution","read from dev","post_processing"]
#legend = ["Read from file", "Write to device", "Pattern matching execution","Read from device","Post-procesing"]
legend = ["CPU energy","GPU energy"]
labels = fancy_names
#lgd = plot_bars(ax,kernels,labels,"Versions", legend, [], stdz, show_legend=False, on_top=False)
lgd = plot_bars(ax,kernels,labels,"Versions", legend, [], stdz, show_legend=True, on_top=True)
plt.autoscale(axis='x',tight=True)

#name="/home/odroid/chasty-dfc-benchmarks/plots/energy_stacked.pdf"
name="/Users/mpastyl/clone_dfc_odroid_results/chasty-dfc-bench-and-backup/plots/energy_stacked.pdf"
plt.savefig(name,bbox_extra_artists=(lgd,), bbox_inches = "tight")
#plt.savefig(name, bbox_inches = "tight")
subprocess.Popen("pdfcrop "+name+" "+name,shell=True)
#subprocess.Popen("pdfcrop")

plt.show()

print "Hybrid (gpu+cpu) vs AC (gpu+cpu))", float(cpu_en[0] + gpu_en[0])/(cpu_en[5] +gpu_en[5])
print "Hybrid (gpu+cpu) vs PFAC (gpu+cpu))", float(cpu_en[2] + gpu_en[2])/(cpu_en[5] +gpu_en[5])


print "ac cpu " ,cpu_en[0]+gpu_en[0]
print "dfc cpu" , cpu_en[1]+gpu_en[1]
print "pfac gpu ",cpu_en[2]+gpu_en[2]
print "dfc gpu ", cpu_en[3]+gpu_en[3]
print "dfc gpu vec ", cpu_en[4]+gpu_en[4]
print "hybrid ", cpu_en[5]+gpu_en[5]
print "hybrid vec", cpu_en[6]+gpu_en[6]

print "improvement", float(cpu_en[0]+gpu_en[0])/(cpu_en[0]+gpu_en[0])
print "improvement", float(cpu_en[0]+gpu_en[0])/(cpu_en[1]+gpu_en[1])
print "improvement", float(cpu_en[0]+gpu_en[0])/(cpu_en[2]+gpu_en[2])
print "improvement", float(cpu_en[0]+gpu_en[0])/(cpu_en[3]+gpu_en[3])
print "improvement", float(cpu_en[0]+gpu_en[0])/(cpu_en[4]+gpu_en[4])
print "improvement", float(cpu_en[0]+gpu_en[0])/(cpu_en[5]+gpu_en[5])
print "improvement", float(cpu_en[0]+gpu_en[0])/(cpu_en[6]+gpu_en[6])
