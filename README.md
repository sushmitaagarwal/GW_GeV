# GeV point searches over extended sky patches
Here we conduct an extended search for gamma-ray sources over wide regions of the sky using Fermi-LAT, an all-sky monitoring telescope. This code is incorporated in the thesis titled 'Probing the Origins of Variable Gamma-Ray
Emission in Relativistic Astrophysical Jets' in Chapter 6 : GeV point searches over extended sky patches.
The details of the code can be found in the thesis here: https://drive.google.com/file/d/1Kifsr9wuw4NEWwHvufFv-706AhdlqJRx/view?usp=sharing


## Steps to follow to run the code:
1. Edit the configuration.yaml file with the lalsky maps and multiorder GW maps and other setting to use in analysis
2. Run sky_localization_credible.ipynb to get the list of RA, DEC to get the pointings within 90% credible patch. THis will be saved in ra_dec_list.txt
3. Now run download_data.py
	|| python download_data.py
4. Run sky_coverage.ipynb to get the times of observation with appropriate theta and zenith cut. This is saved in valid_time_bnNONE.txt
5. copy this file in each of the downloaded grids data using:
	|| for d in ./*.*_*.*_*.* ; do
	       cp ../valid_time_bnNONE.txt .
	   done 

5. Run the shell script on each folder corresponsing to each pointing. You can also set the time periods you wish to analyse by changing tstart and tend in ./Impfiles/valid_time_bnNone.txt. By default the code analyzed 0-10ks in 20ks bins
	|| . ./run_RunFermi_script.sh
