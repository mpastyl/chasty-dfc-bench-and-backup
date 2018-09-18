
#ALWAYS make sure you have checked out the correct branches on both dirs
#Also check your parameters (e.g. in CMakeLists)
version="df_size_combined_total_cost"
script_name="./scripts/dfc.sh"
tags="none"

dfc_bench_dir="/home/odroid/dfc-benchmark-libraries/"
log_dir="/home/odroid/chasty-dfc-benchmarks/logs/"
log_name=$version"_throughput."$(date +%Y-%m-%d_%H:%M)".log"

datasets=(\
	  /home/odroid/Downloads/dfc-datasets/outside_http.pcap \
	 )
patterns=(\
	  /home/odroid/Downloads/dfc-rulesets/http_related_rules \
	 )
repeat=5
#df_sizes=("0x100" "0x1000" "0x10000" "0x100000" "0x1000000")
df_sizes=("0x1000" "0x2000" "0x4000" "0x8000" "0x10000" "0x20000" "0x40000" "0x80000")

cd $dfc_bench_dir
for data in "${datasets[@]}"
do
	for pat in "${patterns[@]}"
	do
		#for i in `seq 1 $repeat`
		for df_size in "${df_sizes[@]}"
		do
			sed -i -e "s/DF_LIMIT/$df_size/g" /home/odroid/dfc-opencl/src/shared.h
			echo $version $data $pat
			res=$($script_name $pat $data)
			dev_write="$(echo $res| grep -oP "OpenCL write to device: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			dev_read="$(echo $res| grep -oP "OpenCL read from device: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			kernel_exec="$(echo $res| grep -oP "OpenCL executing kernel: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			#might need to change on non-Heterogeneous verions
			post_proc="$(echo $res| grep -oP "CPU process matches \(Heterogeneous version\): [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			file_read="$(echo $res| grep -oP "Reading data from file: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			echo "version: "$version "tags: "$tags "patterns: "$pat "dataset: "$data "kernel_exec: "$kernel_exec "dev_write: "$dev_write "dev_read: "$dev_read "post_proc: "$post_proc "file_read: "$file_read "df_size: "$df_size
			echo "version: "$version "tags: "$tags "patterns: "$pat "dataset: "$data "kernel_exec: "$kernel_exec "dev_write: "$dev_write "dev_read: "$dev_read "post_proc: "$post_proc "file_read: "$file_read "df_size: "$df_size >> $log_dir$log_name
			sed -i -e "s/DF_MASK ($df_size -1)/DF_MASK (DF_LIMIT -1)/g" /home/odroid/dfc-opencl/src/shared.h
		done
	done
done
