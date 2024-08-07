input_folder="/afs/cern.ch/work/k/kmotaama/public/top_exotic/analysis/config/input_files"

for d in $(ls -d $input_folder/*)
do
    
        #python analysis_stage2.py --input $d
        ./train.py --xc config/xgboost/config_xgboost.yml --input $d
        ./train.py --xc config/xgboost/config_xgboost.yml --input $d --infer
        ./stats/prepare.py --input $d   
    
done