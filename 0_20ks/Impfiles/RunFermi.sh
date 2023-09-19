#cp data/gll_ft2_tr_bn*_v00.fit sc.fits
#cp data/gll_ft1_tr_bn*_v00.fit ph.fits
#cp data/gll_cspec_tr_bn*.rsp GRB.rsp

#python3 codeForNavigationPLot.py

python LAT_analysis_xmasGRB.py $1 > log_LAT.log
#cat log_LAT.log | grep "|"  > GRB_LAT_analysisResults.txt

