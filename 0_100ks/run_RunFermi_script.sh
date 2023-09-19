cwd=$(pwd)
pwd
for d in ./*.*_*.*_*.* ; do
    echo "$d"
    cd $d
    pwd
    ls RunFermi.sh
    . ./RunFermi.sh bnNone 
    cd ./Results
    cp ../log_LAT.log .
    sh collect_results.sh
    cd ..
    cd ..
done  
