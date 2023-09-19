import subprocess

def gtdolike(tsmin, emin, emax, flemin, flemax, clul, irfs,liketype_ty, ra, dec, triggername):
  
  
  #assert clul < 1.0, "The confidence level for the upper limit (clul) must be < 1"
  
  from GtBurst import dataHandling
  from GtBurst.angularDistance import getAngularDistance
  
  eventfile="FT1_filt.fits"
  #"FT1_filtered.fits"
  rspfile="GRB.rsp"
  ft2file="sc.fits"
  liketype='unbinned'
  xmlmodel="GRB_model.xml"
  expomap="FT1_expMap.fits"
  ltcube="FT1_ltCube.fits"
  optimize='no'
  
  
  fin = open(xmlmodel, "rt")
  #read file contents to string
  data = fin.read()
  str1='free="1" max="10.0" min="0.1"'
  str2='free="1" max="10.0" min="0.1"'
  
  
  
  #replace all occurrences of the required string
  data = data.replace(str1, str2)
  
    
  #close the input file
  fin.close()
  #open the input file in write mode
  fin = open("data.txt", "wt")
  #overrite the input file with the resulting data
  fin.write(data)
  #close the file
  fin.close()
  
  
  fin = open("data.txt", "rt")
  #read file contents to string
  data1 = fin.read()


  
  str3='free="0" max="10.0" min="0.0"'
  
  
  #replace all occurrences of the required string
  
  data1 = data1.replace(str3, str2)
    
  #close the input file
  fin.close()
  #open the input file in write mode
  fin = open("data.txt", "wt")
  #overrite the input file with the resulting data
  fin.write(data)
  #close the file
  fin.close()
  
  
  subprocess.call("mv data.txt GRB_model.xml", shell=True)

  
  
  LATdata                     = dataHandling.LATData(eventfile,rspfile,ft2file)
  try:
    print (" TRYINGGGG" )  
    if(liketype=='unbinned'):
      outfilelike, sources        = LATdata.doUnbinnedLikelihoodAnalysis(xmlmodel,tsmin,expomap=expomap,ltcube=ltcube,emin=flemin,emax=flemax, clul=clul)
      print ("Doneeeeee")
    else:
      #Generation of spectral files and optimization of the position is
      #not supported yet for binned analysis
      
      if(spectralfiles=='yes'):
      
        print("\nWARNING: you specified spectralfiles=yes, but the generation of spectral files is not supported for binned analysis\n")
        spectralfiles               = 'no'
      
      if(optimize=='yes'):
      
        print("\nWARNING: you specified optimize=yes, but position optimization is not supported for binned analysis\n") 
        optimize                    = 'no'
      
      outfilelike, sources        = LATdata.doBinnedLikelihoodAnalysis(xmlmodel,tsmin,expomap=expomap,ltcube=ltcube,emin=flemin,emax=flemax, clul=clul)
  except GtBurstException as gt:
    raise gt
  except:
    raise


  #irfs, ra, dec, triggername
  #Transfer information on the source from the input to the output XML
  #irfs                        = (irfs)
  #ra                          = (ra)
  #dec                         = (dec)
  #triggername                 = (triggername)
  


  
 
  try:
    grb                         = [x for x in sources if x.name.lower().find(name.lower())>=0][0]
    grb_TS                      = grb.TS
  except:
    #A model without GRB
    print("\nWarning: no GRB in the model!")
    grb_TS                      = -1
  pass
  
  if(irfs is None):
    print("\n\nWARNING: could not read IRF from XML file. Be sure you know what you are doing...")
  else:
    dataHandling._writeParamIntoXML(outfilelike,IRF=irfs,OBJECT=triggername,RA=ra,DEC=dec)
  pass

  spectralfiles="no"
  if(spectralfiles=='yes'):
    phafile,rspfile,bakfile   = LATdata.doSpectralFiles(outfilelike)
  pass
  
  localizationMessage         = ''
  bestra                      = ''
  bestdec                     = ''
  poserr                      = ''
  distance                    = ''
  figure="no"
  skymap=None  
  showmodelimage='no'
  if(figure is not None):
        
    #Assume we have an X server running
    #Now display the results
    likemsg = "Log(likelihood) = %s" %(LATdata.logL)
    
    for src in sources:
      weight                  = 'bold'
      
      if(src.type=='PointSource'):
        if(src.TS > 4):
          #detectedSources.append(src)
          if(src.name.find('FGL')<0):
            #GRB
            grbF         = float(src.flux)
            grbeF           = float(src.fluxError)
            grbI           = float(src.photonIndex)
            grbeI           = float(src.photonIndexError)
          print (grbF, grbeF, grbI, grbeI)    
          return grbF, grbeF, grbI, grbeI, src.TS

        else:
          
            grbF         = float(1e-13)
            grbeF           = float(1e-13)
            grbI           = float(1.0)
            grbeI           = float(1.0)
            print (grbF, grbeF, grbI, grbeI)    
            return grbF, grbeF, grbI, grbeI, src.TS
   
  print(localizationMessage)
