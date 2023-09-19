#!/usr/bin/env python

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


from GtBurst import dataHandling
from GtBurst import bkge
import sys, copy
from GtBurst.my_fits_io import pyfits

import os, numpy
from GtBurst import commandDefiner
from GtBurst import LikelihoodComponent
from GtBurst import dataHandling
from GtBurst.GtBurstException import GtBurstException
import sys
import os
from GtBurst import commandDefiner
from GtBurst.GtBurstException import GtBurstException
from matplotlib.figure import Figure
from GtBurst.my_fits_io import pyfits

import numpy,math
import re
import yaml
import subprocess

GRB=str(sys.argv[1])
#subprocess.call("rm filt_"+GRB+".fits", shell=True)
#subprocess.call("rm sc_"+GRB+".fits ph_"+GRB+".fits *.rsp", shell=True)
#subprocess.call("cp ../data/"+GRB+"/gll_ft1_tr_"+GRB+"_v00.fit ph.fits", shell=True)
#subprocess.call("cp ../data/"+GRB+"/gll_ft2_tr_"+GRB+"_v00.fit sc.fits", shell=True)
#subprocess.call("cp ../data/"+GRB+"/gll_cspec_tr_"+GRB+"_v00.rsp GRB.rsp", shell=True)

    
    
def supply_info(filename):
 ft1 = pyfits.open(filename)

 t_ = ft1['EVENTS'].data.field("TIME")
 print ('t_',t_)
 
 ra= ft1['EVENTS'].data.field("RA")
 print ('ra', ra)
 dec= ft1['EVENTS'].data.field("DEC")
 print ('dec', dec)

 #hdul = fits.open(fits_image_filename)
 OBJECT= "none" #ft1[0].header['OBJECT']
 
 TT= time___ #ft1[0].header['TRIGTIME']
 t = numpy.array([x - TT for x in t_])   
 print (t)
    
 RA_OBJ= ra___
 DEC_OBJ= dec___
 

 return (OBJECT, TT, RA_OBJ, DEC_OBJ, t, ra, dec, max(t))


triggername_, tt, RA_OBJ, DEC_OBJ, tA, rA, decA, Ts=supply_info("gll_ft1_tr_bnnnn_v00.fits") 


def read_one_block_of_yaml_data(filename):
    with open(f'{filename}.yaml','r') as f:
        output = yaml.safe_load(f)
    #print(output) 
    return (output)
    
file_contents=read_one_block_of_yaml_data('configuration')

print (file_contents['source']['triggertime'])


triggername = GRB
trigTime    = float(file_contents['source']['triggertime'])
ra          = float(file_contents['source']['RA'])
dec         = float(file_contents['source']['DEC'])

tstart      = float(file_contents['source']['triggertime'])
tstop       = Ts

rad         = float(file_contents['selections']['rad'])
irfs        = file_contents['selections']['irf']
zenithCut   = float(file_contents['selections']['zmax'])
Emin        = float(file_contents['selections']['emin'])
Emax        = float(file_contents['selections']['emax'])
skybin      = float(file_contents['selections']['skybinsize'])
thetacut    = float(file_contents['selections']['thetamax'])
strategy    = file_contents['selections']['strategy']

emin=30.0
emax=300000.0
roicut      = rad
xref        = RA_OBJ
yref        = DEC_OBJ
roi         = rad
particle_model= file_contents['model']['particlemodel']
galactic_model= file_contents['model']['galacticmodel']
source_model= file_contents['model']['sourcemodel']
fglmode= file_contents['model']['fglmode']
  
tsmin       = float(file_contents['likelihood']['tsmin'])
optimizeposition=file_contents['likelihood']['optimizeposition']
spectralfiles= file_contents['likelihood']['spectralfiles']
liketype =file_contents['likelihood']['liketype']
clul        = float(file_contents['likelihood']['clul'])
flemin      = float(file_contents['likelihood']['flemin'])
flemax      = float(file_contents['likelihood']['flemax'])



import numpy as np
fl=np.loadtxt("valid_time_"+GRB+".txt", "float")

for lines in fl:
  #if (lines[0]>0):
    tmin=lines[0]
    tmax=lines[1]
    makeFileDIR={'tmin': (tmin), 'tmax':(tmax), 'filteredeventfile' : "FT1_filt.fits", 'rspfile' : 'GRB.rsp', 'ft2file' : 'sc.fits',         'SkyMapfile': 'FT1_skymap.fits', 'expomap' : 'FT1_expMap.fits', 'ltcube'  : 'FT1_ltCube.fits', 'xmlmodel'  : 'GRB_model.xml',         'showmodelimage' : 'no', 'optimize'  : 'no', 'spectralfiles' : 'no', 'tsmin' : (tsmin),         'skymap' : 'no', 'liketype' : 'unbinned', 'clobber' : 'no', 'verbose' : 'no',         'flemin' : str(flemin), 'flemax' : str(flemax), 'clul' : str(clul),             'particle_model'  : 'isotr template',             'galactic_model'  : 'template (fixed norm.)', 'source_model'  : 'PowerLaw2',             'xmlmodel' : 'GRB_model.xml', 'triggername'  : (triggername), 'ft2file'  : 'sc.fits',             'fglmode'   : 'complete', 'ra' : (ra), 'dec'  : (dec), 'particle_model'  : 'isotr template',              'galactic_model'  : 'template (fixed norm.)', 'source_model'  : 'PowerLaw2',             'filteredeventfile'  : 'FT1_filt.fits', 'xmlmodel' : 'GRB_model.xml',             'trigTime'  : (trigTime), 'ft2file'  : 'sc.fits', 'fglmode'   : 'complete',              'tstart': str(tmin), 'tstop': (tmax), 'irf': str(irfs), 'roi': (roi) , 'strategy': str(strategy)}
    xmlDICT= {'ra' : (ra), 'dec'  : (dec), 'particle_model'  : str(particle_model),              'galactic_model'  : str(galactic_model), 'source_model'  : str(source_model),             'filteredeventfile'  : 'FT1_filt.fits', 'xmlmodel' : 'GRB_model.xml',             'triggername'  : (triggername), 'ft2file'  : 'sc.fits', 'fglmode'   : str(fglmode),              'tstart': str(tmin), 'tstop': (tmax), 'irf': str(irfs), 'roi': (roi) }

    
    
    print ("|times:\t", lines[0],"\t", lines[1])
    
    my_precious(Emin,Emax,lines[0], lines[1],rad,irfs,thetacut,skybin,roicut,zenithCut,tsmin,clul, makeFileDIR, xmlDICT)
