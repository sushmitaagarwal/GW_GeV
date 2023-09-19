from gt_apps import *
import os
current_directory=os.getcwd()
print (current_directory)
lines=current_directory.split("/")
print (lines)
lines=lines[8].split("_")
print (lines)
phfile="ph.fits"
scfile="sc.fits"
Emin=100.
Emax=100000.
Tstart=599884271.054916
Tstop=599974271.054916
ra=lines[0]
dec=lines[1]
print (ra,dec)

def run():

    evtbin["evfile"]=phfile
    evtbin["scfile"]=scfile
    evtbin["outfile"]="out.pha"
    evtbin["algorithm"]="PHA1"
    evtbin["ebinalg"]="LOG"
    evtbin["emin"]= Emin
    evtbin["emax"]= Emax
    evtbin["enumbins"]=30
    evtbin["denergy"]=0.0
    evtbin["ebinfile"]="__energyBins.fits"
    evtbin["tbinalg"]="LIN"
    evtbin["tstart"]= Tstart
    evtbin["tstop"]=  Tstop
    evtbin["dtime"]=4.096
    evtbin["tbinfile"]="NONE"
    evtbin["snratio"]=0.0
    evtbin["lcemin"]=0.0
    evtbin["lcemax"]=0.0
    evtbin["nxpix"]=121
    evtbin["nypix"]=121
    evtbin["binsz"]=0.2
    evtbin["coordsys"]="CEL"
    evtbin["xref"]=ra
    evtbin["yref"]=dec
    evtbin["axisrot"]=0.0
    evtbin["rafield"]="RA"
    evtbin["decfield"]="DEC"
    evtbin["proj"]="AIT"
    evtbin["hpx_ordering_scheme"]="RING"
    evtbin["hpx_order"]=3
    evtbin["hpx_ebin"]="yes"
    evtbin["hpx_region"]=""
    evtbin["evtable"]="EVENTS"
    evtbin["sctable"]="SC_DATA"
    evtbin["efield"]="ENERGY"
    evtbin["tfield"]="TIME"
    evtbin["chatter"]=2
    evtbin["clobber"]="yes"
    evtbin["debug"]="no"
    evtbin["gui"]="no"
    evtbin["mode"]="ql"
    
    evtbin.run()
 
    rspgen["respalg"]="PS"
    rspgen["specfile"]="out.pha"
    rspgen["scfile"]=scfile
    rspgen["outfile"]="GRB.rsp"
    rspgen["irfs"]="P8R3_TRANSIENT020E_V2"
    rspgen["sctable"]="SC_DATA"
    rspgen["resptpl"]="DEFAULT"
    rspgen["chatter"]=2
    rspgen["clobber"]="yes"
    rspgen["debug"]="no"
    rspgen["gui"]="no"
    rspgen["mode"]="ql"
    rspgen["time"]=0.0
    rspgen["thetacut"]=70.0
    rspgen["dcostheta"]=0.025
    rspgen["phinumbins"]=1
    rspgen["ebinalg"]="LOG"
    rspgen["efield"]="ENERGY"
    rspgen["emin"]=70.0
    rspgen["emax"]=100000.0
    rspgen["enumbins"]=30
    rspgen["denergy"]=50.0
    rspgen["ebinfile"]="NONE"
    
    rspgen.run()
    
    
run()
