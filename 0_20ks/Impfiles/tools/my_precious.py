from GtBurst import commandDefiner
from tools.performStandardCut_Biswa import *
from tools.gtdolike import *
from GtBurst import LikelihoodComponent
import matplotlib.pyplot as plt
import GtApp







def gtbuildxmlmodel(**kwargs):
  run(**kwargs)
pass



def my_precious(Emin, Emax,tmin, tmax,rad,irfs,thetacut,skybin,roicut,zenithCut,tsmin,clul, makeFileDIR, xmlDICT):
 performStandardCut_Biswa(Emin, Emax,thetacut, roicut,irfs,zenithCut,rad, gtmktime_do=True,**makeFileDIR)
 gtbuildxmlmodel(**xmlDICT)

 emin=Emin
 emax=Emax
 clul=clul
 tsmin=tsmin
 irfs=irfs
 
 for key in list(makeFileDIR.keys()):
            if (key == "flemin"):
                flemin = float(makeFileDIR[key])
            elif (key == "flemax"):
                flemax = float(makeFileDIR[key])
            elif (key == "tsmin"):
                tsmin = float(makeFileDIR[key])
            elif (key == "liketype"):
                liketype = makeFileDIR[key]
            
 for key in list(xmlDICT.keys()):
            if (key == "emin"):
                emin = xmlDICT[key]
            elif (key == "emax"):
                emax = int(xmlDICT[key])
            elif (key == "ra"):
                ra = str(xmlDICT[key])
            elif (key == "dec"):
                dec = str(xmlDICT[key])
            elif (key == 'rad'):
                rad=str(xmlDICT[key])
            elif (key == 'triggername'):
                triggername=str(xmlDICT[key])  
 
 l=gtdolike(tsmin, emin, emax, flemin, flemax, clul, irfs,liketype, ra, dec, triggername)
 plt.close()
 return l
