import astropy
import numpy 
import healpy
import matplotlib
import numpy as np
import healpy as hp
from pylab import rcParams
#from astropy.stats import bayesian_blocks
import random
import matplotlib as pl
import matplotlib.pyplot as colors
import matplotlib.lines as mlines
import GtBurst
from matplotlib.legend_handler import HandlerLine2D
from matplotlib import gridspec
from GtBurst.dataCollector import *
from GtBurst import dataHandling
from GtBurst.commands.gtllebin import gtllebin
from GtBurst.GtBurstException import *
import numpy
import subprocess
from  GtBurst.dataHandling import date2met
from GtBurst.my_fits_io import pyfits
from gt_apps import *
import yaml
from GtBurst import html2text

#Set a global timeout of 10 seconds for all web connections
import socket
socket.setdefaulttimeout(60)
pl.rcParams['ytick.minor.visible'] =True
pl.rcParams['xtick.minor.visible'] = True
pl.rcParams['xtick.top'] = True
pl.rcParams['ytick.right'] = True
pl.rcParams['font.size'] = '15'
pl.rcParams['legend.fontsize'] = '10'
pl.rcParams['legend.borderaxespad'] = '1.9'
pl.rcParams['figure.titlesize'] = 'small'
pl.rcParams['figure.titlesize'] = 'small'
pl.rcParams['xtick.major.size'] = '8'
pl.rcParams['xtick.minor.size'] = '5'
pl.rcParams['xtick.major.width'] = '2'
pl.rcParams['xtick.minor.width'] = '1'
pl.rcParams['ytick.major.size'] = '10'
pl.rcParams['ytick.minor.size'] = '6'
pl.rcParams['ytick.major.width'] = '2'
pl.rcParams['ytick.minor.width'] = '1'
pl.rcParams['xtick.direction'] = 'in'
pl.rcParams['ytick.direction'] = 'in'
pl.rcParams['axes.labelpad'] = '10.0'
pl.rcParams['lines.dashed_pattern']=3.0, 1.4
pl.rcParams['lines.dotted_pattern']= 1.0, 0.7
pl.rcParams['xtick.labelsize'] = '15'
pl.rcParams['ytick.labelsize'] = '15'
pl.rcParams['axes.labelsize'] = '19'
pl.rcParams['axes.labelsize'] = '19'
pl.rcParams['xtick.major.pad']='10'
pl.rcParams['xtick.minor.pad']='10'
from  GtBurst.dataHandling import date2met

import pylab
from matplotlib import rc
from matplotlib import gridspec
gs = gridspec.GridSpec(1, 1)
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('axes', linewidth=2.5)
import re, os
import urllib.request, urllib.parse, urllib.error
import html.parser as HTMLParser
import time
import re, os
import sys
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
import numpy
import sys
import os
from GtBurst import commandDefiner
from GtBurst.GtBurstException import GtBurstException
from matplotlib.figure import Figure
from GtBurst.my_fits_io import pyfits
from GtBurst import angularDistance



def supply_info(filename):
 ft1 = pyfits.open(filename)

 t_ = ft1['EVENTS'].data.field("TIME")
 
 ra= ft1['EVENTS'].data.field("RA")
 dec= ft1['EVENTS'].data.field("DEC")

 #hdul = fits.open(fits_image_filename)
 OBJECT= ft1[0].header['OBJECT']
 
 TT= ft1[0].header['TRIGTIME']
 t = numpy.array([x - TT for x in t_])
 
 RA_OBJ=ft1[0].header['RA_OBJ']
 DEC_OBJ=ft1[0].header['DEC_OBJ']  

 return (OBJECT, TT, RA_OBJ, DEC_OBJ, t, ra, dec, max(t))



#striggername_, tt, RA_OBJ, DEC_OBJ, tA, rA, decA, Ts=supply_info("ph.fits") 

def write_yaml_to_file(py_obj,filename):
    with open(f'{filename}.yaml', 'w',) as f :
        yaml.dump(py_obj,f,sort_keys=False) 
    print('Written to file successfully')



def read_one_block_of_yaml_data(filename):
    with open(f'{filename}.yaml','r') as f:
        output = yaml.safe_load(f)
    #print(output) 
    return (output)

def navigation_plot(triggerTime,ra_obj,dec_obj,zenithcut,thetacut):
	Zcut=float(zenithcut)
	Tcut=float(thetacut)
	grbName='nnn'
	ft2file="gll_ft2_tr_bn%s_v00.fits" %(grbName)

	ft2 = pyfits.open(ft2file)

	ra_scz = ft2['SC_DATA'].data.field("RA_SCZ")
	dec_scz = ft2['SC_DATA'].data.field("DEC_SCZ")
	ra_zenith = ft2['SC_DATA'].data.field("RA_ZENITH")
	dec_zenith = ft2['SC_DATA'].data.field("DEC_ZENITH")
	time = ft2['SC_DATA'].data.field("START")
	time = numpy.array([x - triggerTime for x in time])
	ft2.close()

	zenith = [angularDistance.getAngularDistance(x[0], x[1], ra_obj, dec_obj) for x in zip(ra_zenith, dec_zenith)]
	zenith = numpy.array(zenith)
	theta = [angularDistance.getAngularDistance(x[0], x[1], ra_obj, dec_obj) for x in zip(ra_scz, dec_scz)]
	theta = numpy.array(theta)


	print ("time, zenith", time, zenith)



	# mask out data gaps do they will appear as gaps in the plots
	mask = (time - numpy.roll(time, 1) > 40.0)
	for idx in mask.nonzero()[0]:
		time = numpy.insert(time, idx, time[idx - 1] + 1)
		zenith = numpy.insert(zenith, idx, numpy.nan)
		theta = numpy.insert(theta, idx, numpy.nan)
		time = numpy.insert(time, idx + 1, time[idx + 1] - 1)
		zenith = numpy.insert(zenith, idx + 1, numpy.nan)
		theta = numpy.insert(theta, idx + 1, numpy.nan)
	pass
	print('ft2         =',ft2file)
	print('zenith @ T0 =',zenith[time>0][0])
	print('theta  @ T0 =',theta[time>0][0])
	    
	figure = plt.figure(figsize=[4, 4], dpi=150)
	figure.set_facecolor("#FFFFFF")
	figure.suptitle("Navigation plots")
	# Zenith plot
	subpl1 = figure.add_subplot(211)
	subpl1.set_xlabel("Time since trigger (s)")
	subpl1.set_ylabel("Source Zenith angle (deg)")
	subpl1.set_ylim([min(zenith - 12) - 0.1 * min(zenith - 12), max([max(zenith + 20), 130])])
	subpl1.plot(time, zenith, '--', color='blue')
	msk = numpy.isnan(zenith)
	stdidx = 0

	try:
		for idx in msk.nonzero()[0][::2]:
			subpl1.fill_between(time[stdidx:idx], zenith[stdidx:idx] - 15, zenith[stdidx:idx] + 15,color='gray', alpha=0.5, label='15 deg ROI')
			subpl1.fill_between(time[stdidx:idx], zenith[stdidx:idx] - 12, zenith[stdidx:idx] + 12,color='lightblue', alpha=0.5, label='12 deg ROI')
			subpl1.fill_between(time[stdidx:idx], zenith[stdidx:idx] - 10, zenith[stdidx:idx] + 10,color='green', alpha=0.5, label='10 deg ROI')
			stdidx = idx + 2
		pass
		subpl1.fill_between(time[stdidx + 1:], zenith[stdidx + 1:] - 15, zenith[stdidx + 1:] + 15,color='gray', alpha=0.5, label='15 deg ROI')
		subpl1.fill_between(time[stdidx + 1:], zenith[stdidx + 1:] - 12, zenith[stdidx + 1:] + 12,color='lightblue', alpha=0.5, label='12 deg ROI')
		subpl1.fill_between(time[stdidx + 1:], zenith[stdidx + 1:] - 10, zenith[stdidx + 1:] + 10,color='green', alpha=0.5, label='10 deg ROI')
	except:
		subpl1.fill_between(time, zenith - 15, zenith + 15,color='gray', alpha=0.5, label='15 deg ROI')
		subpl1.fill_between(time, zenith - 12, zenith + 12,color='lightblue', alpha=0.5, label='12 deg ROI')
		subpl1.fill_between(time, zenith - 10, zenith + 10,color='green', alpha=0.5, label='10 deg ROI')
	tt3 = subpl1.axhline(100, color='red', linestyle='--')
	p1 = plt.Rectangle((0, 0), 1, 1, color="green", alpha=0.5)
	p2 = plt.Rectangle((0, 0), 1, 1, color="lightblue", alpha=0.5)
	p3 = plt.Rectangle((0, 0), 1, 1, color="gray", alpha=0.5)
	zl = subpl1.axhline(1000, color='blue', linestyle='--')
	subpl1.legend([zl, tt3, p1, p2, p3],["Source", 'Zenith = 100 deg', "10 deg ROI", "12 deg ROI", "15 deg ROI"],prop={'size': 5}, ncol=2)

	# Theta plot
	subpl2 = figure.add_subplot(212, sharex=subpl1)
	subpl2.set_xlabel("Time since trigger (s)")

	subpl2.set_ylabel("Source off-axis angle (deg)")
	subpl2.set_ylim([min(theta) - 0.1 * min(theta), max([max(theta), 95])])
	subpl2.plot(time, theta, '--')
	subpl2.axhline
	plt.savefig(final_directory+"/navigate.pdf", dpi=600)
	plt.close()



	print (len(time), len(theta), len(zenith))

	TIME=[]
	for i in range(len(zenith)):
		if((zenith[i]<Zcut) & (theta[i]<Tcut)):
			TIME.append(time[i])
		#print(time[i])
	#print (TIME)
	s_=str(float(TIME[0]-1.0) )+"\\"       
	for j in range(len(TIME)-1):
		if ((TIME[j+1]-TIME[j]) > 31.):
			s_=s_+str(TIME[j])+'//'+str(TIME[j+1])+'\\'

	s1=s_+"\\"+str(float(TIME[j+1]+1))
	s__=s1.replace("\\", "\t")
	s___=s__.replace("//", "\n")

	print (s___)

	file_InValidInterval=open("ValidIntervals.txt", 'w')
	file_InValidInterval.write(s___)
	file_InValidInterval.close()


def run():
	evtbin["evfile"]= "ph.fits"  #phfile
	evtbin["scfile"]= "sc.fits"
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
	rspgen["scfile"]="sc.fits"
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

def mjd_fermi_met(mjd): 
    fermi_met = (mjd-51910.0000235)/1.15740739296e-05
    #fermi_met=(8.64000000e+04 * mjd) -4.48502399e+09 
    return fermi_met

#print (mjd_fermi_met(57279.41024786981))

def retrieve_url(filename):
    if (filename=="default"):
        print ('YESSSS')
        temporaryFileName           = "__temp_query_result.html"
        try:
            os.remove(temporaryFileName)
        except:
            pass
        pass

        urllib.request.urlretrieve("https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi",temporaryFileName)
    else:
        temporaryFileName           = filename
        try:
            os.remove(temporaryFileName)
        except:
            pass
        pass

        urllib.request.urlretrieve("https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi",temporaryFileName)
  


class DivParser(HTMLParser.HTMLParser):
    def __init__(self,desiredDivName):
        HTMLParser.HTMLParser.__init__(self)
        self.recording                      = 0
        self.data                           = []
        self.desiredDivName                 = desiredDivName

    def handle_starttag(self, tag, attributes):
        if tag != 'div':
            return
        if self.recording:
            self.recording                   += 1
            return
        for name, value in attributes:
            if name == 'id' and value == self.desiredDivName:
                break
        else:
            return
        self.recording                      = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.recording:
            self.recording                   -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)
pass


def getFTP(ra,dec,roi,tstart,tstop,triggerTime,timetype,what='Extended'):
    #Re-implementing this
    #This will complete automatically the form available at
    #https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi
    #After submitting the form, an html page will inform about
    #the identifier assigned to the query and the time which will be
    #needed to process it. After retrieving the query number,
    #this function will wait for the files to be completed on the server,
    #then it will download them
    grbName='nnn'
    parent=None
    #Save parameters for the query in a dictionary
    parameters                  = {}
    parameters['coordfield']    = "%s,%s" %(ra,dec)
    parameters['coordsystem']   = "J2000"
    parameters['shapefield']    = "%s" %(roi)
    parameters['timefield']     = "%s,%s" %(tstart,tstop)
    parameters['timetype']      = "%s" %(timetype)
    parameters['energyfield']   = "100,100000"
    parameters['photonOrExtendedOrNone'] = 'Extended'
    parameters['destination']   = 'query'
    parameters['spacecraft']    = 'checked'


    print("Query parameters:")
    for k,v in iter(list(parameters.items())):
            print(("%30s = %s" %(k,v)))

    postData = urllib.parse.urlencode(parameters)
    #print ('postData',postData)
    url = "https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi?%s" % postData
    print ("url query: %s" %url)

    urllib.request.urlcleanup()

    with urllib.request.urlopen(url) as f:
        html=f.read().decode('utf-8')
        #print (html)
        #urllib.request.urlretrieve(url, temporaryFileName)
        pass

    print("\nAnswer from the LAT data server:\n")
    text                        = html#html2text.html2text(html.encode('utf-8').strip()).split("\n")



    if("".join(text).replace(" ","")==""):
            raise GtBurstException(1,"Problems with the download. Empty answer from the LAT server. Normally this means that the server is ingesting new data, please retry in half an hour or so.")
    text                        = [x for x in text if x.find("[") < 0 and 
                                                      x.find("]") < 0 and 
                                                      x.find("#") < 0 and 
                                                      x.find("* ") < 0 and
                                                      x.find("+") < 0 and
                                                      x.find("Skip navigation")<0]
    text                        = [x for x in text if len(x.replace(" ",""))>1]
    print(("\n".join(text)))
    print("\n\n")
    #os.remove(temporaryFileName)
    if(" ".join(text).find("down due to maintenance")>=0):
        raise GtBurstException(12,"LAT Data server looks down due to maintenance.")

    parser                      = DivParser("sec-wrapper")
    parser.feed(html)

    if(parser.data==[]):
        parser                      = DivParser("right-side")
        parser.feed(html)
    pass

    try: 
        estimatedTimeLine           = [x for x in parser.data if x.find("The estimated time for your query to complete is")==0][0]
        estimatedTimeForTheQuery    = float(re.findall("The estimated time for your query to complete is ([0-9]+) seconds",estimatedTimeLine)[0])
    except:
        raise GtBurstException(1,"Problems with the download. Empty or wrong answer from the LAT server (see console). Please retry later.")
    pass
    print("Estimated Time For The Query....:",estimatedTimeForTheQuery)

    try:

        httpAddress                 = [x for x in parser.data if x.find("http://fermi.gsfc.nasa.gov") >=0][0]

    except IndexError:

        # Try https
        httpAddress                 = [x for x in parser.data if x.find("https://fermi.gsfc.nasa.gov") >=0][0]

    #Now periodically check if the query is complete
    startTime                   = time.time()
    timeout                     = 1.5*max(5.0,float(estimatedTimeForTheQuery)) #Seconds
    refreshTime                 = 2.0  #Seconds
    #When the query will be completed, the page will contain this string:
    #The state of your query is 2 (Query complete)
    endString                   = "The state of your query is 2 (Query complete)"
    #Url regular expression
    regexpr                     = re.compile("wget (.*.fits)")

    #Build the window for the progress
    if(parent is None):
        #No graphical output
            root                 = None
    else:
          #make a transient window
            root                 = Toplevel()
            root.transient(parent)
            root.grab_set()
            l                    = Label(root,text='Waiting for the server to complete the query (estimated time: %s seconds)...' %(estimatedTimeForTheQuery))
            l.grid(row=0,column=0)
            m1                    = Meter(root, 500,20,'grey','blue',0,None,None,'white',relief='ridge', bd=3)
            m1.grid(row=1,column=0)
            m1.set(0.0,'Waiting...')
    pass


    links                       = None
    fakeName                    = "__temp__query__result.html"
    while(time.time() <= startTime+timeout):
        if(root is not None):
            if(estimatedTimeForTheQuery==0):
                m1.set(1)
            else:
                m1.set((time.time()-startTime)/float(max(estimatedTimeForTheQuery,1)))
        sys.stdout.flush()
        #Fetch the html with the results
        try:
            (filename, header)        = urllib.request.urlretrieve(httpAddress,fakeName)
        except socket.timeout:
            urllib.request.urlcleanup()
            if(root is not None):
                root.destroy()
            raise GtBurstException(11,"Time out when connecting to the server. Check your internet connection, or that you can access https://fermi.gsfc.nasa.gov, then retry")
        except:
            urllib.request.urlcleanup()
            if(root is not None):
                root.destroy()
            raise GtBurstException(1,"Problems with the download. Check your connection or that you can access https://fermi.gsfc.nasa.gov, then retry.")
        pass

        f                         = open(fakeName)
        html                      = " ".join(f.readlines())
        status                    = re.findall("The state of your query is ([0-9]+)",html)[0]
        #print("Status = %s" % status)
        if(status=='2'):
        #Get the download link
            links                   = regexpr.findall(html)
            break
        f.close()
        os.remove(fakeName)
        urllib.request.urlcleanup()
        time.sleep(refreshTime)
    pass  

    if(root is not None):
        root.destroy()

    remotePath                = "data/LAT/queries/"
    if(links is not None):
        filenames                 = [x.split('/')[-1] for x in links]
        #print (filenames)
        try:
            self.downloadDirectoryWithFTP(remotePath,filenames=filenames)
        except Exception as e:
        #try:
            #downloadDirectoryWithFTP(remotePath,filenames=filenames)

            for ff in filenames:
                try:
                    print('Trying with curl...')
                    #makeLocalDir()
                    cwd=os.getcwd()
                    print ('working directory in loop', cwd)
                    #os.chdir(r"%s" %localRepository)
                    #dataHandling.runShellCommand("curl -LO %s%s -o %s/." %("https://fermi.gsfc.nasa.gov/FTP/fermi/data/lat queries/",ff,self.localRepository),True)
                    dataHandling.runShellCommand("curl -LO %s%s " %("https://fermi.gsfc.nasa.gov/FTP/fermi/data/lat/queries/",ff),True)
                    os.chdir(r"%s" % cwd)
                except:
                    raise e
                pass
            pass
        pass    
    else:
      raise GtBurstException(1,"Could not download LAT Standard data")
    pass

    #Rename the files to something neater...
    newFilenames              = {}
    for f in filenames:
      #EV or SC?
      suffix                  = f.split("_")[1]
      if (suffix.find("EV00") >= 0):
        suffix = 'ft1'
      elif (suffix.find("EV") >= 0):
        pass
      elif(suffix.find("SC")>=0):
        suffix                = 'ft2'
      else:
        raise GtBurstException(13,"Could not understand the type of a downloaded file (%s)" %(f))
      newfilename             = os.path.join(cwd,"gll_%s_tr_bn%s_v00.fits" %(suffix,grbName))
      localPath               = os.path.join(cwd,f)
      
      os.rename(localPath,newfilename)
      newFilenames[suffix]    = newfilename
    pass
    
    ###########################
    if('ft1' in list(newFilenames.keys()) and 'ft2' in list(newFilenames.keys())):
      dataHandling._makeDatasetsOutOfLATdata(newFilenames['ft1'],newFilenames['ft2'],
                                             grbName,tstart,tstop,
                                             ra,dec,triggerTime,
                                             cwd,
                                             cspecstart=-1000,
                                             cspecstop=1000)
    
#  pass

#pass    
    print ('filenames ', filenames)  
    return (filenames)
    
#========================================
    
from  astropy.utils.data import download_file

file_contents_main=read_one_block_of_yaml_data('configuration')
print ('lalmap', str(file_contents_main['GWevent']['lalmap']))

#final_skymap = download_file(remote_url= "https://www.gw-openscience.org/GW150914data/P1500227/LALInference_skymap.fits.gz",cache = True)
final_skymap = download_file(remote_url= (file_contents_main['GWevent']['lalmap']),cache = True)

current_directory = os.getcwd()
print (current_directory)
#=========================================

prob, header = hp.read_map(filename=final_skymap, h=True, verbose=False)
print(header)

header = dict(header)

#Whdn was the GW event trigger. EXtract this information from the GW fits file.
trigger_time_mjd=header['MJD-OBS']
print ('Date of observation of GW event (MJT)',trigger_time_mjd)


data_obs=header['DATE-OBS']
print ('Trigger time for GW event (CT)', data_obs)

date_obs=data_obs.split('T')[0]
time_obs=data_obs.split('T')[1]
date_total=date_obs+' '+time_obs
trigger_time_fermi_met=date2met(date_total)

# What is the present working directory
home_directory=os.getcwd()

#============================================

#List of desired RA,DEC values extracted from the GW patch using sky_localization.ipynb
ra_dec_file=np.genfromtxt('ra_dec_list.txt')

#=============================================

timetype = 'MET'
data_length=int(file_contents_main['GWevent']['datalength'])            #10ks
data_b4_trigger=int(file_contents_main['GWevent']['timeb4trigger'])
region_of_interest=int(file_contents_main['GWevent']['downloadroi'])
Emin=int(file_contents_main['selections']['emin'])
Emax=int(file_contents_main['selections']['emax'])

num_ra_dec=ra_dec_file.ndim

#If number of ra,dec to download ==1 , run this
if (num_ra_dec==1):
	ra = float(ra_dec_file[0])
	dec = float(ra_dec_file[1])
	roi = region_of_interest
	triggerTime=(float(trigger_time_fermi_met))-data_b4_trigger
	tstart=float(triggerTime)
	tstop=float(tstart + data_length+data_b4_trigger)
	    
	info=np.array([ra, dec,tstart, tstop, (tstop-tstart)]).T
	    
	    #retrieve_url(filename="default")
	    
	current_directory = os.getcwd()
	new_folder="%.4f_%.4f_%.1f"%(ra, dec, triggerTime)
	final_directory = os.path.join(current_directory, new_folder)

	if not os.path.exists(final_directory):
	  os.makedirs(final_directory)
	    
	os.chdir(r"%s" %final_directory)
	    
	filenames = getFTP(ra,dec,roi,tstart,tstop,triggerTime,timetype,what='Extended')
	#os.chdir(r"%s" %current_directory)
	print ('Number of files', len(filenames))
	    
	print (filenames)
	number_of_files=len(filenames)
	print (number_of_files)
	    
	if (number_of_files==2):
	  phfile=filenames[0]
	  print (phfile)
	  print (type(phfile))
	  
	  scfile=filenames[1]
	  print (scfile)
	  print (type(scfile))
	    
	  subprocess.call("cp gll_ft1_tr_bnnnn_v00.fits  ph.fits", shell=True)
	  subprocess.call("cp gll_ft2_tr_bnnnn_v00.fits  sc.fits", shell=True)
	  subprocess.call("cp gll_cspec_tr_bnnnn_v00.rsp  GRB.rsp", shell=True)
	  subprocess.call("cp gll_cspec_tr_bnnnn_v00.pha  out.pha", shell=True)
	  subprocess.call("cp -r ../configuration.yaml  .", shell=True)
	  
	  file_contents=read_one_block_of_yaml_data('configuration')
	  file_contents['source']['triggertime']=str(triggerTime)
	  file_contents['source']['RA']=str(ra)
	  file_contents['source']['DEC']=str(dec)
	  write_yaml_to_file(file_contents, 'configuration')
		#write_yaml_to_file(data, 'configuration')    
	   
	    
		
		
	  subprocess.call('cat ../LAT_analysis_xmasGRB.py | sed -e "s/time___/'+str(triggerTime)+'/g"> l_ ', shell=True)
	  subprocess.call('cat l_ | sed -e "s/ra___/'+str(ra)+'/g"> l__ ', shell=True)
	  subprocess.call('cat l__ | sed -e "s/dec___/'+str(dec)+'/g"> LAT_analysis_xmasGRB.py; rm l_ l__ ', shell=True)
	  
	  subprocess.call('cp -r ../Impfiles/* .   ', shell=True)
	  
	  #subprocess.call('. RunFermi.sh bnNone', shell=True)
	  
	  #subprocess.call('cp log_LAT.log  Results/   ', shell=True)
	  
	if (number_of_files>2):
	  scfile=filenames[-1]
	  with open('events_list.txt', 'w') as f:
	    for i in range (0,number_of_files-1):
	      f.write(final_directory+phfile[i]+'\n')
	    f.close()
   	
	navigation_plot(trigger_time_fermi_met-data_b4_trigger,ra,dec, file_contents['selections']['zmax'], file_contents['selections']['thetamax'])
	Tstart=tstart
	Tstop=tstop
	    #run()
	os.chdir(r"%s" %current_directory)

# if list of RA, DEC > 1, run this
elif (num_ra_dec > 1):
	for i in range(len(ra_dec_file)):
	    ra = float(ra_dec_file[i][0])
	    dec = float(ra_dec_file[i][1])
	    roi = region_of_interest
	    triggerTime=(float(trigger_time_fermi_met))-data_b4_trigger
	    tstart=float(triggerTime)
	    tstop=float(tstart + data_length+data_b4_trigger)
	    
	    info=np.array([ra, dec,tstart, tstop, (tstop-tstart)]).T
	    
	    #retrieve_url(filename="default")
	    
	    current_directory = os.getcwd()
	    new_folder="%.4f_%.4f_%.1f"%(ra, dec, triggerTime)
	    final_directory = os.path.join(current_directory, new_folder)

	    if not os.path.exists(final_directory):
	      os.makedirs(final_directory)
	    
	    os.chdir(r"%s" %final_directory)
	    
	    filenames = getFTP(ra,dec,roi,tstart,tstop,triggerTime,timetype,what='Extended')
	    #os.chdir(r"%s" %current_directory)
	    print ('Number of files', len(filenames))
	    
	    print (filenames)
	    number_of_files=len(filenames)
	    print (number_of_files)
	    
	    if (number_of_files==2):
	      phfile=filenames[0]
	      print (phfile)
	      print (type(phfile))
	      
	      scfile=filenames[1]
	      print (scfile)
	      print (type(scfile))
	      
	      subprocess.call("cp gll_ft1_tr_bnnnn_v00.fits  ph.fits", shell=True)
	      subprocess.call("cp gll_ft2_tr_bnnnn_v00.fits  sc.fits", shell=True)
	      subprocess.call("cp gll_cspec_tr_bnnnn_v00.rsp  GRB.rsp", shell=True)
	      subprocess.call("cp gll_cspec_tr_bnnnn_v00.pha  out.pha", shell=True)
	      subprocess.call("cp -r ../configuration.yaml  .", shell=True)
	      
	      file_contents=read_one_block_of_yaml_data('configuration')
	      file_contents['source']['triggertime']=str(triggerTime)
	      file_contents['source']['RA']=str(ra)
	      file_contents['source']['DEC']=str(dec)
	      write_yaml_to_file(file_contents, 'configuration')
		#write_yaml_to_file(data, 'configuration')    
	   
	    
		
		
	      subprocess.call('cat ../LAT_analysis_xmasGRB.py | sed -e "s/time___/'+str(triggerTime)+'/g"> l_ ', shell=True)
	      subprocess.call('cat l_ | sed -e "s/ra___/'+str(ra)+'/g"> l__ ', shell=True)
	      subprocess.call('cat l__ | sed -e "s/dec___/'+str(dec)+'/g"> LAT_analysis_xmasGRB.py; rm l_ l__ ', shell=True)
	      
	      subprocess.call('cp -r ../Impfiles/* .   ', shell=True)
	      
	      #subprocess.call('. RunFermi.sh bnNone', shell=True)
	      
	      #subprocess.call('cp log_LAT.log  Results/   ', shell=True)
	      
	    if (number_of_files>2):
	      scfile=filenames[-1]
	      with open('events_list.txt', 'w') as f:
	        for i in range (0,number_of_files-1):
	          f.write(final_directory+phfile[i]+'\n')
	        f.close()
   	
	    navigation_plot(trigger_time_fermi_met-data_b4_trigger,ra,dec, file_contents['selections']['zmax'], file_contents['selections']['thetamax'])
	    Tstart=tstart
	    Tstop=tstop
	    #run()
	    os.chdir(r"%s" %current_directory)
	
