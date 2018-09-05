
#ALWAYS make sure you have checked out the correct branches on both dirs
#Also check your parameters (e.g. in CMakeLists)
version="ac-snort"
script_name="./scripts/ac-snort.sh"
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

cd $dfc_bench_dir
for data in "${datasets[@]}"
do
	for pat in "${patterns[@]}"
	do
		for i in `seq 1 $repeat`
		do
			echo $version $data $pat
			res=$($script_name $pat $data /dev/null)
			total_time="$(echo $res| grep -oP "Total search time: [+-]?([0-9]*[.])?[0-9]+"|cut -d ":" -f2)"
			echo "version: "$version "tags: "$tags "patterns: "$pat "dataset: "$data "kernel_exec: "$total_time 
			echo "version: "$version "tags: "$tags "patterns: "$pat "dataset: "$data "kernel_exec: "$total_time >> $log_dir$log_name
		done
	done
done
