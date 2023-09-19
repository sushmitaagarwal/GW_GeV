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



def _yesOrNoToBool(value):      
  if(value.lower()=="yes"):
    return True
  elif(value.lower()=="no"):
    return False
  else:
    raise ValueError("Unrecognized clobber option. You can use 'yes' or 'no'")    
  pass
pass

class Message(object):
  def __init__(self,verbose):
    self.verbose              = bool(verbose)
  pass
  
  def __call__(self,string):
    if(self.verbose):
      print(string)
pass   



executableName                = "gtbuildxmlmodel"
version                       = "1.0.0"
shortDescription              = "Produce the XML model for the likelihood analysis."
author                        = "G.Vianello, giacomov@slac.stanford.edu"
thisCommand                   = commandDefiner.Command(executableName,shortDescription,version,author)

#Define the command parameters
thisCommand.addParameter("filteredeventfile","Input event list (FT1 file)",commandDefiner.MANDATORY,partype=commandDefiner.DATASETFILE,extension="fit")
thisCommand.addParameter("ra","R.A. of the point source (probably a GRB or the Sun)",commandDefiner.MANDATORY)
thisCommand.addParameter("dec","Dec of the point source (probably a GRB or the Sun)",commandDefiner.MANDATORY)
thisCommand.addParameter("triggername","Name of the source",commandDefiner.OPTIONAL,'GRB')
thisCommand.addParameter("particle_model",'''Model for the particle background (possible values: 
                                            'isotr with pow spectrum', 'isotr template', 'none')''',commandDefiner.MANDATORY,
                                         'isotr with pow spectrum',
                                         possiblevalues=['isotr template', 'isotr with pow spectrum',  'none', 'bkge'])#possibleParticleModels
thisCommand.addParameter("galactic_model",'''Model for the Galactic background (possible values:
                                             'template (fixed norm.)', 'template', 'none')''',commandDefiner.MANDATORY,
                                         'template (fixed norm.)',
                                         possiblevalues=['template (fixed norm.)','template','none'])
thisCommand.addParameter("source_model",'''Spectral model for the new source (GRB or SF).''',
                                           commandDefiner.MANDATORY,
                                         'PowerLaw2',
                                         possiblevalues=list(LikelihoodComponent.availableSourceSpectra.keys()))
thisCommand.addParameter("tstart","",commandDefiner.MANDATORY)
thisCommand.addParameter("tstop","",commandDefiner.MANDATORY)
thisCommand.addParameter("irf","",commandDefiner.MANDATORY)
thisCommand.addParameter("roi","",commandDefiner.MANDATORY)
thisCommand.addParameter("fgl_mode",
'''"fast" = include FGL sources in or around ROI giving at least 1 photons in this
time interval if at their normal flux (use only for GRBs and SFs).
This will turn in a big speed improvement in the likelihood
analysis.\n
"complete" = include all FGL sources in or around ROI''',
                                           commandDefiner.OPTIONAL,
                                         'complete',
                                         possiblevalues=['complete','fast'])


thisCommand.addParameter("ft2file","Spacecraft file (FT2)",commandDefiner.OPTIONAL,partype=commandDefiner.DATASETFILE,extension="fits")
thisCommand.addParameter("xmlmodel","Name for the output file for the XML model",commandDefiner.MANDATORY,partype=commandDefiner.OUTPUTFILE,extension="xml")
thisCommand.addParameter("clobber","Overwrite output file? (possible values: 'yes' or 'no')",commandDefiner.OPTIONAL,"yes")
thisCommand.addParameter("verbose","Verbose output (possible values: 'yes' or 'no')",commandDefiner.OPTIONAL,"yes")



def run(**kwargs):
  if(len(list(kwargs.keys()))==0):
    #Nothing specified, the user needs just help!
    thisCommand.getHelp()
    return
  pass
  
  #Get parameters values
  thisCommand.setParValuesFromDictionary(kwargs)
  try:
    ra                          = thisCommand.getParValue('ra')
    dec                         = thisCommand.getParValue('dec')
    particlemodel               = thisCommand.getParValue('particle_model')
    galacticmodel               = thisCommand.getParValue('galactic_model')
    sourcemodel                 = thisCommand.getParValue('source_model')
    filteredeventfile           = thisCommand.getParValue('filteredeventfile')
    xmlmodel                    = thisCommand.getParValue('xmlmodel')
    triggername                 = thisCommand.getParValue('triggername')
    ft2file                     = thisCommand.getParValue('ft2file')
    fglmode                     = thisCommand.getParValue('fgl_mode')
    tstart                      = thisCommand.getParValue('tstart')
    tstop                       = thisCommand.getParValue('tstop')
    irf                         = thisCommand.getParValue('irf')
    roi                         = thisCommand.getParValue('roi')
    clobber                     = _yesOrNoToBool(thisCommand.getParValue('clobber'))
    verbose                     = _yesOrNoToBool(thisCommand.getParValue('verbose'))
  except KeyError as err:
    print(("\n\nERROR: Parameter %s not found or incorrect! \n\n" %(err.args[0])))
    
    #Print help
    print((thisCommand.getHelp()))
    return
  pass
  
  #Get the IRF from the event file
  try:
    f                             = pyfits.open(filteredeventfile)
  except:
    raise GtBurstException(31,"Could not open filtered event file %s" %(filteredeventfile))
  
  
  #particlemodel                 ='isotr template'
  possibleParticleModels        = ['isotr template', 'isotr with pow spectrum',  'none', 'bkge']
  
  #Lookup table for the models
  models = {}
  if(particlemodel=='isotr with pow spectrum'):
    models['isotr with pow spectrum'] = LikelihoodComponent.IsotropicPowerlaw()
  elif(particlemodel=='isotr template'):
    models['isotr template']          = LikelihoodComponent.IsotropicTemplate(irf)
  pass
  
  if(galacticmodel=='template'):
    models['template']                = LikelihoodComponent.GalaxyAndExtragalacticDiffuse(irf,ra,dec,2.5*roi)
  elif(galacticmodel=='template (fixed norm.)'):
    models['template (fixed norm.)']  = LikelihoodComponent.GalaxyAndExtragalacticDiffuse(irf,ra,dec,2.5*roi)
    models['template (fixed norm.)'].fixNormalization()
  pass
  
  deltat                        = numpy.sum(f['GTI'].data.field('STOP')-f['GTI'].data.field('START'))
  f.close()
  triggertime                   = dataHandling.getTriggerTime(filteredeventfile)
  
  if(irf.lower().find('source')>=0 and particlemodel!='isotr template'):
    raise GtBurstException(6,"Do not use '%s' as model for the particle background in SOURCE class. Use '%s' instead." 
                     %(particlemodel,'isotropic template'))
  
  modelsToUse                   = [LikelihoodComponent.PointSource(ra,dec,triggername,sourcemodel)]
  if(particlemodel!='none'):
    if(particlemodel=='bkge'):
      if(ft2file is None or ft2file==''):
        raise ValueError("If you want to use the BKGE, you have to provide an FT2 file!")
      
      modelsToUse.append(LikelihoodComponent.BKGETemplate(filteredeventfile,
                                                          ft2file,tstart,tstop,triggername,triggertime))
    else:
      modelsToUse.append(models[particlemodel])
  if(galacticmodel!='none'):
    modelsToUse.append(models[galacticmodel])
  
  xml                          = LikelihoodComponent.LikelihoodModel()
  xml.addSources(*modelsToUse)
  xml.writeXML(xmlmodel)
  
  if(fglmode=='complete'):
    
    #Use a very large delta T so that 
    #all FGL sources are included in the
    #xml model
    deltat                     = 1e12
  
  xml.addFGLsources(ra,dec,float(roi)+8.0,xmlmodel,deltat)
    
  
  dataHandling._writeParamIntoXML(xmlmodel,IRF=irf,OBJECT=triggername,RA=ra,DEC=dec)
    
  return 'xmlmodel', xmlmodel
pass

#thisCommand.run = run
