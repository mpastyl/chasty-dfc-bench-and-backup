
#ALWAYS make sure you have checked out the correct branches on both dirs
#Also check your parameters (e.g. in CMakeLists)
version="combined_vec"
script_name="./scripts/dfc.sh"
tags="64TG-10Mbuf"

dfc_bench_dir="/home/odroid/dfc-benchmark-libraries/"
log_dir="/home/odroid/chasty-dfc-benchmarks/logs/"
log_name=$version"_throughput."$(date +%Y-%m-%d_%H:%M)".log"

datasets=(\
          /home/odroid/Downloads/dfc-datasets/outside_http.pcap \
          /home/odroid/Downloads/dfc-datasets/testbed_payload_small \
          /home/odroid/Downloads/dfc-datasets/bigFlows.pcap_small \
          /home/odroid/Downloads/dfc-datasets/random.data_small \
         )
patterns=(\
          /home/odroid/Downloads/dfc-rulesets/http_related_rules \
          /home/odroid/Downloads/dfc-rulesets/emerging_all_5000 \
         )
repeat=5

cd $dfc_bench_dir
for data in "${datasets[@]}"
do
	for pat in "${patterns[@]}"
	do
		for i in `seq 1 $repeat`
		do
			echo $version $data $pat
			res=$($script_name $pat $data)
			dev_write="$(echo $res| grep -oP "OpenCL write to device: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			dev_read="$(echo $res| grep -oP "OpenCL read from device: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			kernel_exec="$(echo $res| grep -oP "OpenCL executing kernel: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			#might need to change on non-Heterogeneous verions
			post_proc="$(echo $res| grep -oP "CPU process matches \(Heterogeneous version\): [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			file_read="$(echo $res| grep -oP "Reading data from file: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			echo "version: "$version "tags: "$tags "patterns: "$pat "dataset: "$data "kernel_exec: "$kernel_exec "dev_write: "$dev_write "dev_read: "$dev_read "post_proc: "$post_proc "file_read: "$file_read
			echo "version: "$version "tags: "$tags "patterns: "$pat "dataset: "$data "kernel_exec: "$kernel_exec "dev_write: "$dev_write "dev_read: "$dev_read "post_proc: "$post_proc "file_read: "$file_read >> $log_dir$log_name
		done
	done
done
