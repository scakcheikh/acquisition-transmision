#!/usr/bin/env python

#--------------------------------------
import time, serial, sys
import subprocess

#Custom files -------------------------
import packageToXML
import scanWrlessForSignal
import fona_3G as fg
from records import ftp_client as ftc
#--------------------------------------

#Configuration, Initialisation, Declaration -----------------------------------
#e.g: "sudo python cntrlr2.py 192.168.1.134 2121" 
user = "user"
psswd = "12345"
serv_addr = sys.argv[1]
port = sys.argv[2]
#ftp2: Remote server
ftp2_addr = "X.X.X.X"
user2 = "username"
psswd2 = "password"
port2 = xx
#-----
xml_file_created = 0
xml_file_sent = 0
coordinate = {'lat':0.0, 'long':0.0, 'date':'', 'time':'', 'alt':0.0}
coord_zero = coordinate
bestLink = "None" 
bestSignal = 0


#----------[Setup]--------------------------------------
#Open serial port and enable GPS
fg.openSerial('/dev/ttyUSB2', 9600) #Change accordingly
fg.enableGPS(True)
ftp_agent = ftc.connectToFTPServer(serv_addr, port, user, psswd)
ftp_agent_public =  ftc.connectToFTPServer(ftp2_addr, port2, user2, psswd2)
#-----------------------------------------------------
if fg.isGPSOn() == True:
	while 1:
		#--------------------------------------
		#----||--Data acquisition--||------
		#--------------------------------------
		coordinate['lat'],coordinate['long'],coordinate['date'],coordinate['time'],coordinate['alt'] = fg.getGPS()		
		#Proceed if received actual gps coordinates
		if (coordinate['lat'] != 0.0) and (coordinate['long'] != 0.0):
			#-------------------------------------------
			#----||--Package data in xml file --||------
			#-------------------------------------------
			packageToXML.packageToXML(xml_file_created, coordinate)
			xml_file_created += 1 
	 	
			#--------------------------------------
			#----||--Apply security layer--||------
			#--------------------------------------
			#
			#
			#
			#

			#----------------------------
			#----||--Scan links--||------
			#----------------------------
			wlinks = {}
			#Get 3G'RSSI
			modemSignal = fg.getRSSI()
			wlinks.update({"3GdBm-m":modemSignal})
			#WIFI RSSI scan	
			ps = subprocess.Popen(('iwlist', 'wlan0', 'scan'), stdout=subprocess.PIPE)
			scanWrlessForSignal.wifiSignal(ps.stdout, wlinks)
			ps.wait()

			#----------------------------------
			#----||--Choose best link--||------
			#----------------------------------
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			print "Scanned links:\n"
			for link,val in wlinks.iteritems():
				print link +':'+ str(val) +" dBm"
                                if (abs(val) < abs(bestSignal)) or (bestSignal == 0):
					bestLink = link
					bestSignal = val 
			print "--------------------------------------------\n"
			print "Best link for transmission: ---{"+ str(bestLink) +":"+ str(bestSignal) + " dBm }---\n" 
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                        blnklast = bestLink[len(bestLink)-1]

			#-----------------------------------------------
			#----||--Send file over tftp to server--||------
			#-----------------------------------------------
			while xml_file_sent < xml_file_created:
                          xml_file = "./records/record_"+str(xml_file_sent)+".xml"
                          if blnklast == 'm': #Then send via 3G
                            print "SEND TO PUBLIC"
                            ftc.upload(ftp_agent_public, xml_file, True)
                          else:
                            ftc.upload(ftp_agent, xml_file, False)
                          #ftc.upload(ftp_agent, xml_file, False)  
			  xml_file_sent +=1

            #----------------------------------------
			#----||-- Wait for next fetch--||------
			#----------------------------------------
			#
			#
			#
			time.sleep(10) #1s
		else:
            time.sleep(.1) #100ms
