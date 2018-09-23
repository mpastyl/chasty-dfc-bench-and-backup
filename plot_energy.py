import sys
import matplotlib.pyplot as plt
import subprocess
from plotters_energy import plot_bars
import numpy as np

fancy_names = [ \
            "AC (CPU)", \
            "DFC (CPU)", \
            "PFAC (GPU)", \
            "DFC (GPU)", \
            #"DFC Vect (GPU)", \
            "HYBRID (GPU)", \
            #"HYBRID Vect (GPU)"\
			]


ac_en = "a15-watt    841.601 a17-watt     55.473 gpu-watt     47.336 mem-watt     20.583 Total_energy 964.993"

dfc_cpu_en = "a15-watt    913.411 a17-watt     55.706 gpu-watt     47.770 mem-watt     16.990 Total_energy 1033.877"

pfac_en = "a15-watt    322.534 a17-watt     52.246 gpu-watt    137.496 mem-watt     24.778 Total_energy 537.054"

dfc_en = "a15-watt    398.396 a17-watt     67.109 gpu-watt    205.917 mem-watt     34.317 Total_energy 705.739"

hybrid_en = "a15-watt    323.180 a17-watt     50.954 gpu-watt    110.878 mem-watt     20.988 Total_energy 506.0"


ALL = [ac_en, dfc_cpu_en, pfac_en, dfc_en, hybrid_en]

total_en = []
for v in ALL:
    x = float(v.split("Total_energy ")[1])
    print x
    total_en.append(x)

kernels = [[x] for x in total_en]
print kernels
stdz = [[0]*len(kernels[0])]*len(kernels)

FIG_SIZE=(7,3.5)
fig , ax = plt.subplots(1,1,figsize=FIG_SIZE)
#legend = ["read_from_file","write to dev","execution","read from dev","post_processing"]
#legend = ["Read from file", "Write to device", "Pattern matching execution","Read from device","Post-procesing"]
legend = fancy_names
labels = [""]
lgd = plot_bars(ax,kernels,labels,"Versions", legend, [], stdz, show_legend=True, on_top=False)

name="/home/odroid/chasty-dfc-benchmarks/plots/energy.pdf"
plt.savefig(name,bbox_extra_artists=(lgd,), bbox_inches = "tight")
subprocess.Popen("pdfcrop "+name+" "+name,shell=True)
subprocess.Popen("pdfcrop")

plt.show()

