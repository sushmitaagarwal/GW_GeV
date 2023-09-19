cwd=$(pwd)
pwd
for d in ./*.*_*.*_*.* ; do
    cp ../valid_time_bnNONE.txt . 
    echo "$d"
    cd $d
    pwd
    ls RunFermi.sh
    . ./RunFermi.sh bnNONE
    cd ./Results
    cp ../log_LAT.log .
    sh collect_results.sh
    cd ..
    cd ..
done  
