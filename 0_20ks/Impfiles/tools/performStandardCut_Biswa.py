#!/usr/bin/env python
#!/usr/bin/env fermi
from GtApp import *

#!/usr/bin/env python
# coding: utf-8



# In[ ]:





# In[19]:


import datetime
import glob
import multiprocessing
import random
import re
import shutil
import subprocess
import time
import numpy
import xml.etree.ElementTree as ET
from contextlib import contextmanager

import BinnedAnalysis
import UnbinnedAnalysis
from GtBurst.wcs_wrap import pywcs
import scipy.optimize

from GtBurst.my_fits_io import pyfits

import gt_apps as my_apps
import GtApp
from GtBurst import IRFS
from GtBurst import LikelihoodComponent
from GtBurst import angularDistance
from GtBurst import version
from GtBurst.Configuration import Configuration
from GtBurst.GtBurstException import GtBurstException
from GtBurst.commands.gtllebin import gtllebin
from GtBurst.statMethods import *

from tools.my_precious import *
from tools.performStandardCut_Biswa import *
from tools.run import *
from tools.gtdolike import *
from tools.MakeRequiredFiles import *

#filtFile=FT1_filt.fits
#SkyMapfile=FT1_skymap.fits
#ltCubeFile='FT1_ltCube.fits'   
#expMapFile='FT1_expMap.fits'      
    





#!/usr/bin/env python

from GtBurst import dataHandling
from GtBurst import bkge
import sys, copy
from GtBurst.my_fits_io import pyfits

import os, numpy
from GtBurst import commandDefiner
from GtBurst import LikelihoodComponent
from GtBurst import dataHandling
from GtBurst.GtBurstException import GtBurstException

# In[ ]:

# In[43]:

#! /usr/bin/env python

import sys
import os
from GtBurst import commandDefiner
from GtBurst.GtBurstException import GtBurstException
from matplotlib.figure import Figure
from GtBurst.my_fits_io import pyfits

import numpy,math
import re

def performStandardCut_Biswa(Emin, Emax,thetaCut, roicut,irf_name,zenithcut,rad_int, **kwargs):

    
        rootName='FT1'
        ft2File="sc.fits"
        eventFile="ph.fits"
        strategy = 'time'
        gtmktime_do=True
        print (gtmktime_do)
        print ('gtmktime',gtmktime_do)
        gtselect = GtApp("gtselect")

        gtmktime = GtApp("gtmktime")
        originalEventFile="ph.fits"
        irf=irf_name
        # Use the evtype
        if (irf.lower().find("p8") >= 0):

            evtype = 3

        else:

            evtype = 'INDEF'

        for key in list(kwargs.keys()):
            if (key == "strategy"):
                strategy = kwargs[key]
            elif (key == "evtype"):
                evtype = int(kwargs[key])
            elif (key == "tmin"):
                tstart = float(kwargs[key])
            elif (key == "tmax"):
                tstop = float(kwargs[key])
            elif (key == "expomap"):
                expomap = str(kwargs[key])
            elif (key == "ltcube"):
                ltcube = str(kwargs[key])
            elif (key == 'filteredeventfile'):
                outfileselect=str(kwargs[key])
            elif (key == "ra"):
                ra = str(kwargs[key])
            elif (key == "dec"):
                dec = str(kwargs[key])
            elif (key == 'rad'):
                rad=str(kwargs[key])
                
            elif (key == "irf"):
                irf = str(kwargs[key])
            elif (key == "zenithcut"):
                zenithcut = str(kwargs[key])
            elif (key == 'trigTime'):
                trigTime=str(kwargs[key])  
            #SkyMapfile, ltCubeFile, expMapFile
            #elif (key == 'SkyMapfile'):
                
        pass

 #expomap, ltcube, SkyMapFile

        # Get tstart and tstop always in MET
        tstart = float(tstart) + int(float(tstart) < 231292801.000) * float(trigTime)
        tstop = float(tstop) + int(float(tstop) < 231292801.000) * float(trigTime)
        ra = float(ra)
        dec = float(dec)
        emin = Emin
        emax = Emax
        zenithCut = zenithcut
        rad= rad_int
        Emin=emin
        Emax=emax
        xref=ra
        yref=dec
        # Check that the FT2 file covers the time interval requested
        f = pyfits.open(ft2File)
        ft2max = max(f['SC_DATA'].data.STOP)
        ft2min = min(f['SC_DATA'].data.START)
        f.close()
        ft2max = float(ft2max) + int(float(ft2max) < float(231292801.000)) * float(trigTime)
        ft2min = float(ft2min) + int(float(ft2min) < float(231292801.000)) * float(trigTime)

        if (ft2min >= float(tstart)):
            stderr.write(
                "\n\nWARNING: Spacecraft file (FT2 file) starts after the beginning of the requested interval. Your start time is now %s (MET %s).\n\n" % (
                ft2min - trigTime, ft2min))
            tstart = ft2min
            time.sleep(2)
        if (ft2max <= float(tstop)):
            stderr.write(
                "\n\nWARNING: Spacecraft file (FT2 file) stops before the end of the requested interval. Your stop time is now %s (MET %s).\n\n" % (
                ft2max - trigTime, ft2max))
            tstop = ft2max
            time.sleep(2)
        pass

        if (tstop <= tstart):
            raise GtBurstException(14, "tstop=%s <= tstart=%s: wrong input or no data coverage for this interval" % (
            tstop, tstart))

        if (not eventFile):
            raise RuntimeError("You cannot select by time if you don't provide a FT1 file.")
	

        if (gtmktime_do==True):
            gtmktime['scfile'] = ft2File
            if (strategy == "time"):
                filt = "(DATA_QUAL>0 || DATA_QUAL==-1) && LAT_CONFIG==1 && IN_SAA!=T && LIVETIME>0"

                if (zenithCut < 180):

                    filt += " && (ANGSEP(RA_ZENITH,DEC_ZENITH,%s,%s)<=(%s-%s))" % (ra, dec, zenithCut, rad)

                else:

                    print("\nNo Zenith cut used\n")

                gtmktime['roicut'] = "no"
            elif (strategy == "events"):
                filt = "(DATA_QUAL>0 || DATA_QUAL==-1) && LAT_CONFIG==1 && IN_SAA!=T && LIVETIME>0"
                gtmktime['roicut'] = "no"
            else:
                raise RuntimeError("Strategy must be either 'time' or 'events'")

            if (thetaCut != 180.0):
                filt += " && (ANGSEP(RA_SCZ,DEC_SCZ,%s,%s)<=%s - %s)" % (ra, dec, thetaCut, rad)
            pass

            print ("===============GTMKTIME YESSS======================")
            gtmktime['filter'] = filt
            gtmktime['evfile'] = "ph.fits"
            outfilemk = "%s_mkt.fit" % (rootName)
            gtmktime['outfile'] = outfilemk
            gtmktime['apply_filter'] = 'yes'
            gtmktime['overwrite'] = 'no'
            gtmktime['header_obstimes'] = 'yes'
            gtmktime['tstart'] = float(tstart)
            gtmktime['tstop'] = float(tstop)
            gtmktime['clobber'] = 'yes'
            try:
                gtmktime.run()
                print ('DONE')
            except BaseException as e:
                raise GtBurstException(22, "gtmktime failed: %s" % str(e))
        else:
            outfilemk = originalEventFile

        # Get the reprocessing version
        f = pyfits.open(originalEventFile)
        reprocessingVersion = str(f[0].header['PROC_VER']).replace(" ", "")
        f.close()
        print(("\nUsing %s data\n" % (reprocessingVersion)))

        gtselect['infile'] = outfilemk
        if (roicut):
            gtselect['ra'] = ra
            gtselect['dec'] = dec
            gtselect['rad'] = rad
        else:
            gtselect['ra'] = 'INDEF'
            gtselect['dec'] = 'INDEF'
            gtselect['rad'] = 'INDEF'
        
        gtselect['tmin'] = tstart
        gtselect['tmax'] = tstop
        gtselect['emin'] = Emin
        gtselect['emax'] = Emax
        gtselect['zmin'] = 0.0
        gtselect['zmax'] = zenithCut

        if (irf.lower() in list(IRFS.IRFS.keys()) and IRFS.IRFS[irf].validateReprocessing(str(reprocessingVersion))):
            irf = IRFS.IRFS[irf]
        else:
            raise ValueError(
                "Class %s not known or wrong class for this reprocessing version (%s)." % (irf, reprocessingVersion))
        pass

        gtselect['evclass'] = irf.evclass

        try:
        
            gtselect['evclsmin'] = 0
            gtselect['evclsmax'] = 1000
        
        except KeyError:
            
            # This happens with the new version of the ST (> 11-00-00)
            # do nothing, these parameters were here for Pass 6 compatibility (they are useless)
            pass
        
        # This try/except is to preserve compatibility with the
        # old science tools, which didn't have the evtype parameter
        if ('evtype' in list(gtselect.keys())):
            gtselect['evtype'] = evtype
        pass

        gtselect['convtype'] = -1
        gtselect['clobber'] = "yes"
        #outfileselect = FiltFile_biswa
        gtselect['outfile'] = outfileselect
        try:
            gtselect.run()
        except BaseException as e:
            raise GtBurstException(23, "gtselect failed for unknown reason: %s " % str(e))

        # Now write a keyword which will be used by other methods to recover ra,dec,rad,emin,emax,zcut
        f = pyfits.open(outfileselect, 'update')
        nEvents = len(f['EVENTS'].data.TIME)
        f[0].header.set('_ROI_RA', "%8.4f" % float(ra))
        f[0].header.set('_ROI_DEC', "%8.4f" % float(dec))
        f[0].header.set('_ROI_RAD', "%8.4f" % float(rad))
        f[0].header.set('_TMIN', "%50.10f" % float(tstart))
        f[0].header.set('_TMAX', "%50.10f" % float(tstop))
        f[0].header.set('_EMIN', "%s" % float(emin))
        f[0].header.set('_EMAX', "%s" % float(emax))
        f[0].header.set('_ZMAX', "%12.5f" % float(zenithCut))
        f[0].header.set('_STRATEG', strategy)
        f[0].header.set('_EVTYPE', evtype)
        f[0].header.set('_IRF', "%s" % irf.name)
        f[0].header.set('_REPROC', '%s' % reprocessingVersion)
        f[0].header.set('_THETAC', '%12.5f' % float(thetaCut))





        # Use the filtered event list as eventfile now
        eventFile = outfileselect
        print(("\nSelected %s events." % (nEvents)))
        f.close()
        print ('file name', type(eventFile)) 
        spacecraft_file='sc.fits'
        #SkyMapfile = str(kwargs['SkyMapfile'])
        
        MakeRequiredFiles(xref, yref, emin, emax, outfileselect, str(kwargs['SkyMapfile']), ltcube, expomap)
            #expomap, ltcube, SkyMapFile
 #filtFile=FT1_filt.fits
 #SkyMapfile=FT1_skymap.fits
 #ltCubeFile='FT1_ltCube.fits'   
 #expMapFile='FT1_expMap.fits'
        
        
        return outfileselect, nEvents
