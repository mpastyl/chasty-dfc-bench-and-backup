
fix="2018-09-20"
cd logs

new_logs=$(ls *$fix*)
for f in $new_logs
do
	echo $f
	pref=$(echo $f | cut -d "." -f1)
	echo $pref
	cat $f > $pref".log"
done
