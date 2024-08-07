
input_folder="/afs/cern.ch/work/k/kmotaama/public/top_exotic/analysis/combine"
current_dir=$PWD

for d in $(ls -d $input_folder/*)
do
    if [ -d "$d" ]; then
        echo "Running combine for sample $(basename $d)"
        cd $d
        . combine.sh
    fi
    
done

cd $current_dir
