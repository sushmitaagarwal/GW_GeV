import gt_apps as my_apps

def MakeRequiredFiles(xref, yref, emin, emax, filtFile, SkyMapfile, ltCubeFile, expMapFile): 
 my_apps.evtbin['evfile'] = filtFile  #Bin the data for cmap
 my_apps.evtbin['outfile'] = SkyMapfile
 my_apps.evtbin['scfile'] = 'sc.fits'
 my_apps.evtbin['algorithm'] = 'CMAP'
 my_apps.evtbin['ebinalg'] = 'FILE'
 my_apps.evtbin['emin'] = 30.0
 my_apps.evtbin['emax'] = 200000.0
 my_apps.evtbin['enumbins'] = 0
 my_apps.evtbin['denergy'] = 0.0
 my_apps.evtbin['ebinfile'] = '__energyBins.fits'
 my_apps.evtbin['tbinalg'] = "LIN"
 my_apps.evtbin['dtime'] = 4.096
 my_apps.evtbin['nxpix'] = 121
 my_apps.evtbin['nypix'] = 121
 my_apps.evtbin['binsz'] = 0.2
 my_apps.evtbin['coordsys'] = 'CEL'
 my_apps.evtbin['xref'] = xref
 my_apps.evtbin['yref'] = yref 
 my_apps.evtbin['axisrot'] = 0
 my_apps.evtbin['proj'] = 'AIT'

 my_apps.evtbin.run()
 my_apps.expCube['evfile'] = filtFile
 my_apps.expCube['scfile'] = 'sc.fits'
 my_apps.expCube['outfile'] = ltCubeFile
 my_apps.expCube['zmax'] = 180
 my_apps.expCube['dcostheta'] = 0.025
 my_apps.expCube['binsz'] = 1
 my_apps.expCube['phibins'] = 1 
 my_apps.expCube.run()

 my_apps.expMap['evfile'] = filtFile
 my_apps.expMap['scfile'] = 'sc.fits'
 my_apps.expMap['expcube'] = ltCubeFile
 my_apps.expMap['outfile'] = expMapFile
 my_apps.expMap['irfs'] = 'P8R3_TRANSIENT010E_V2'
 my_apps.expMap['srcrad'] = 16.0
 my_apps.expMap['nlong'] = 100
 my_apps.expMap['nlat'] = 100
 my_apps.expMap['nenergies'] = 25
 my_apps.expMap.run() 
