#!/usr/bin/env python

import time, serial, sys
import subprocess

#Custom files ------------------------------------
#import sendXml
import packageToXML
import scanWrlessForSignal
import tftp_client_uu as tcu
#-------------------------------------------------

#Configuration, Initialisation, Declaration -----------------------------------
ser = serial.Serial(
   port='/dev/ttyACM0',
   baudrate = 115200,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)

way = sys.argv[1]
server_addr = sys.argv[2]
tftp_port = sys.argv[3]
stats_file = sys.argv[4]

x =""
i = 0
first_loop = 0
gotGPS = False
xml_file_created = 0
xml_file_sent = 0
coordinate ={"longitude":0.0, "latitude":0.0, "altitude":0.0, "time":""}
date = time.strftime("%Y-%m-%d", time.gmtime())
bestLink = "None" 
bestSignal = 0

#------------------------------------------------
while 1:
  #--------------------------------------
  #----||--Data acquisition--||------
  #--------------------------------------
  x=str(ser.readline())
  print x
  #Every X milli seconds do
  if len(x) >= 4 and x[0] == "l" and x[1] == "i" and x[2] == "s" and x[3] == "t":
    if i:
      time.sleep(10)
    if i == 0:
      i=1
    ser.write('g') # send char to arduino
  
  #-------------------------------------------
  #----||--Package data in xml file --||------
  #-------------------------------------------
  if len(x) >= 4 and x[0] == "l" and x[1] == "a" and x[2] == "t" and x[3] == ":":
    gotGPS = True 
    coordinate["latitude"] = float(x.split(',')[0].split(':')[1])
    coordinate["longitude"] = float(x.split(',')[1].split(':')[1])
    coordinate["altitude"] = float(x.split(',')[4].split(':')[1])
    coordinate["time"] = time.strftime("%H:%M:%S", time.gmtime())
    packageToXML.packageToXML(i, date, coordinate)
    i +=1
    xml_file_created += 1 
    		
  #--------------------------------------
  #----||--Apply security layer--||------
  #--------------------------------------
  #
  #
  #
  #

  if len(x) >= 4 and x[0] == "R" and x[1] == "S" and x[2] == "S" and x[3] == "I" and gotGPS:
	gotGPS = False
	wlinks = {}	
	#----------------------------
	#----||--Scan links--||------
	#----------------------------
	#Get 3G RSSI
	cellularSignal = (x.split(':')[1]).strip('\n')
  	#print "3GdBm: "+ 3GSignal + "dBm\n"
	wlinks.update({"3GdBm-m":cellularSignal})
	#WIFI RSSI scan	
	ps = subprocess.Popen(('iwlist', 'wlan0', 'scan'), stdout=subprocess.PIPE)
	scanWrlessForSignal.wifiSignal(ps.stdout, wlinks)
	ps.wait()
		
	#----------------------------------
	#----||--Choose best link--||------
	#----------------------------------
        print "------------------------------------------------\n"
	print "Scanned links:\n"
	for link,val in wlinks.iteritems():
	    print link +':'+ str(val)
	    print '\n'  
	    if val < bestSignal:
		bestLink = link
	        bestSignal = val 
	print "--------------------------------------------------------\n"
  	print "Best link for transmission: ------["+ str(bestLink) +":"+ str(bestSignal) + " dBm ]--->\n" 
	print "--------------------------------------------------------\n"

        #-----------------------------------------------
	#----||--Send file over tftp to server--||------
	#-----------------------------------------------
        while xml_file_sent < xml_file_created:
          xml_file = "./records/record_"+str(xml_file_sent+1)+".xml"
          tcu.sendXML(xml_file, way, server_addr, tftp_port, bestLink, bestSignal, stats_file)
          xml_file_sent +=1	

  
    #----------------------------------------
	#----||--update statistics file--||------
	#----------------------------------------
	#
	#
	#
