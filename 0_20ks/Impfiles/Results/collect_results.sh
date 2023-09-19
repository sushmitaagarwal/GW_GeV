cat log_LAT.log  | grep "|bn"  | awk '{print $7}' | sed 's/|//g' > TS
cat log_LAT.log  | grep "|bn" -A 5 | grep "erg/cm2" | awk '{print  $5, $6}' > EnergyFlux
grep '|bn' --no-group-separator -A2 log_LAT.log | awk 'NR % 3 == 0' | awk '{print  $4, $5}' | sed -e 's/"|"/""/g' > index
cat log_LAT.log  | grep "|times" | awk '{print $2, $3}' > times
cat log_LAT.log | grep "time -p gtselect" | awk '{print $6, $7}' > RADEC

cat log_LAT.log  | grep "|IsotropicTemplate"  | awk '{print $7}' | sed 's/|//g' > TSiso
cat log_LAT.log  | grep "|Iso" -A 3 | grep "erg/cm2" | awk '{print  $5, $6}' | sed 's/|//g' > Fluxiso
cat log_LAT.log  | grep "|Iso" -A 5 | grep "Norm"  | awk '{print $4, $5}' | sed 's/|//g' > Normiso




paste times RADEC EnergyFlux index TS Normiso  Fluxiso TSiso > l

sed -i 's/n.a./0.00/g' l


sed -i 's/|/ /g' l


sed -i 's/flux </-2.0/g'  l

sed -i 's/ra=//g'   l


sed -i 's/dec=//g'  l


mv l LAT_results_0.1-100GeV.txt
rm times RADEC EnergyFlux index TS TSiso Fluxiso Normiso
