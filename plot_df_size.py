import sys
import matplotlib.pyplot as plt
import subprocess
from plotters import plot_bars
import numpy as np

log_total = "logs/df_size_combined_total_cost_throughput.2018-09-20_18:13.log"
log_filtering = "logs/df_size_filtering_total_cost_throughput.2018-09-20_18:11.log"

#log_total = "logs/df_size_combined_total_cost_throughput.2018-09-18_15:06.log"
#log_filtering = "logs/df_size_combined_filtering_cost_throughput.2018-09-18_15:05.log"

names = [ "dfc_size_combined"]
df_sizes = ["0x1000", "0x2000" ,"0x4000", "0x8000", "0x10000", "0x20000", "0x40000", "0x80000"]
df_sizes_kb = [0.5, 1 ,2 ,4 ,8 ,16, 32, 64]

filtering_raw = [\
        41348126, \
        32718846, \
        27348745, \
        24376283, \
        23796704, \
        18603814, \
        14482545, \
        12252649]
total_bytes = 168927947
filtering_ratio = [ 100*x/float(168927947) for x in filtering_raw]

need_correction = [ "ac-snort", "dfc-cpu"]

datasets = ["outside_http.pcap"]
patterns = ["http_related_rules"]

total_cost = []

with open(log_total,'rb') as log:
    for row in log:
        df_size = 0
        v = row.split("version: ")[1].split()[0]
        pat = row.split("patterns: ")[1].split()[0].split('/')[-1]
        dataset = row.split("dataset: ")[1].split()[0].split('/')[-1]
        kernel_exec = float(row.split("kernel_exec: ")[1].split()[0])
        if "df_size" in row:
            df_size = (row.split("df_size: ")[1].split()[0])
        total_cost.append((df_size,kernel_exec))

filtering_cost = []

with open(log_filtering,'rb') as log:
    for row in log:
        df_size = 0
        v = row.split("version: ")[1].split()[0]
        pat = row.split("patterns: ")[1].split()[0].split('/')[-1]
        dataset = row.split("dataset: ")[1].split()[0].split('/')[-1]
        kernel_exec = float(row.split("kernel_exec: ")[1].split()[0])
        if "df_size" in row:
            df_size = (row.split("df_size: ")[1].split()[0])
        filtering_cost.append((df_size,kernel_exec))


print total_cost
time_total = zip(*total_cost)[1]
time_filtering  = zip(*filtering_cost)[1]

#plt.plot(df_sizes_kb,time_total)
#plt.plot(df_sizes_kb,time_filtering)
#plt.plot(time_total)
#plt.plot(time_filtering)
#plt.show()

FIG_SIZE=(6,4)
fig , ax1 = plt.subplots(1,1,figsize=FIG_SIZE)
ax1.plot(time_total,'-v',label='Total execution cost')
ax1.plot(time_filtering,'-^',label='Filtering cost')
ax1.set_xticklabels(df_sizes_kb)
ax1.set_xlabel("Filter size (KB)")
ax1.set_ylabel("Execution time (ms)")
ax1.legend(loc=2)

ax2 = ax1.twinx()
ax2.plot(filtering_ratio,'r-.',label='Hit ratio')
ax2.set_ylabel("Hit ratio (%)")
ax2.legend()

name="/home/odroid/combined_filter_size.pdf"
plt.savefig(name, bbox_inches = "tight")
subprocess.Popen("pdfcrop "+name+" "+name,shell=True)
subprocess.Popen("pdfcrop")
plt.show()

