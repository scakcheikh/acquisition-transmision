#!/usr/bin/env python

import time, serial, sys
from math import floor as m_floor

#Custom files ------------------------------------
#-------------------------------------------------

serGPS = serial.Serial(
   port='/dev/ttyUSB2',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)

x = ''
ok_reply = "OK"
replyBuffer = []
position = {'lat':0.0, 'long':0.0, 'date':'', 'time':'', 'alt':0.0} 
sig = 0.0
sig_int = 0
sig_dec = 0
#---------------SERIAL PROCESSING FUNCTIONS---------------------------------
def flushInput():
	timeoutloop = 40
	while timeoutloop < 40:
		while serGPS.inWaiting():
			serGPS.read(2)
		time.sleep(.1)
		timeoutloop +=1
	serGPS.flushInput()
	#print "FLUSHED"
	
def getReply(at_cmd):
	flushInput()
	returnBuffer = []
	serGPS.write(at_cmd+'\r')
	time.sleep(.1)
	while serGPS.inWaiting():
		tmp = serGPS.read()
		returnBuffer.append(tmp)
		#print ''.join(replyBuffer)
	return  ''.join(returnBuffer)

def parseReplyInf(raw_str):
	
	toParse = (raw_str.split(':'))[1]
	#print toParse
	r1= []
	#r2 = []
	for i in toParse:
		if ord(i) == 13 or ord(i) == 10 or ord(i) == 32:
			continue
		else :
			r1.append(i)
	"""for i in toParse[1]:
		if ord(i) == 13 or ord(i) == 10 or ord(i) == 32:
			continue
		else :
			r2.append(i)"""
	return ''.join(r1)#, ''.join(r2)

def parseGPS(raw_str):
	toParse = raw_str.split(':')
	r1 = []
	count = 0
	for i in toParse[1]:
		if ord(i) == 13 or ord(i) == 10 or ord(i) == 32:
			if count < 2:
				count +=1
				continue
			else:
				break
		r1.append(i)
	return ''.join(r1)

def parseReplyExec(raw_str):
	toParse = raw_str
	r1 = []
	for i in toParse:
		if ord(i) == 13 or ord(i) == 10 or ord(i) == 32:
			continue
		else :
			r1.append(i)
	return ''.join(r1)

def sendCheckReplyInf(at_cmd, ok_reply):
        replyBuffer = []
        while (replyBuffer == []):
          tmp = getReply(at_cmd)
	  replyBuffer = (tmp.split('\r\n'))[1:]
	  print "---@@"
	  print replyBuffer
	  print "@@@---"
	  flushInput()
	  time.sleep(.3)
	  
	r_val = parseReplyInf(replyBuffer[0])
	returned = replyBuffer[2]
	return (returned == ok_reply), r_val

def sendCheckReplyInf2(at_cmd):
	tmp2 = getReply(at_cmd)
	#print "---"
	#print tmp2
	#print "---"
	replyBuffer = (tmp2.split('\r\n'))[1]
	gpsBuffer = parseGPS(replyBuffer)
	return gpsBuffer

def sendCheckReplyExec(at_cmd, ok_reply): #for response like ['AT+CGPS=1\r', 'OK', '']
	tmp = getReply(at_cmd)
	print "*******"
	print tmp.split("\r\n")
        print "*******"
	replyBuffer = (tmp.split("\r\n"))[1]
	
	return (replyBuffer == ok_reply)
	 	
def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

#--------------GPS FUNCTIONS----------------------------------
def openSerial(ttyPORT, bdRate, timeout=1):
	try:
		serGPS = serial.Serial(port=ttyPORT,baudrate=bdRate,timeout= timeout)
		serGPS.open()
		print "Serial port"+ttyPORT+" Ready"
	except Exception, e:
		print "Issue on openining PORT: "+ttyPORT
		print str(e)
		"""if e != 'Port is already open':
			exit()
		else:
			print "Proceeding program ..."""

def closeSerial():
	try:
		serGPS.close()
		print "Serial closed on "+serGPS.port+" !"
	except Exception, e:
		print "Error on closing PORT: "+serGPS.port
		print str(e)
		exit()


def enableGPS(onoff):
	#Get state
	state, gps_state = sendCheckReplyInf("AT+CGPS?\r", ok_reply)
	#print "state:"+ str(state)
	#print "gps:"+str(gps_state)
	if state == False :
		print "GPS probably already activated "
		return False
	elif (onoff == False) and gps_state == "1,1":
		if sendCheckReplyExec("AT+CGPS=0\r", ok_reply)== True:
			time.sleep(2)
			serGPS.read()
			print "GPS deactivated"
			
	elif onoff and gps_state == "0,1":
		if sendCheckReplyExec("AT+CGPS=1\r", ok_reply) == True:
			print "GPS activated"
		time.sleep(.5)
		
	#print "After:---------------"
	#state, gps_state =sendCheckReplyInf("AT+CGPS?\r", ok_reply)
	#print "state:"+ str(state)
	#print "gps:"+str(gps_state)

def isGPSOn():
	state, gps_state = sendCheckReplyInf("AT+CGPS?\r", ok_reply)
	if state == True:
		if gps_state == "1,1":
			return True
		else:
			return False 

def getGPS():
	if isGPSOn() == True:
		gps_data = (sendCheckReplyInf2("AT+CGPSINFO\r"))
		print "--------------"
		print gps_data
		print "--------------"
		if gps_data != ",,,,,,,,":
			tmp = gps_data.split(',')	
			latp = float(tmp[0])
			latd = tmp[1]
			longp = float(tmp[2])
			longd = tmp[3]
			date = tmp[4]
			time = tmp[5]
			alt = float(tmp[6])

			#Converting latitude to minutes to decimal
			deg = m_floor(latp / 100)
			minu = latp - (100 * deg)
			minu /= 60
			deg += minu
			if latd == 'S':
				deg *= -1
			lat = deg

			#Same for longitude
			deg = m_floor(longp / 100)
			minu = longp - (100 * deg)
			minu /= 60
			deg += minu
			if longd == 'W':
				deg *= -1
			longi = deg
			return lat, longi, date, time, alt
		else:
			return 0.0, 0.0, '','',0.0 	

#--------------NETWORK FUNCTIONS----------------------------------
def getRSSI():
	r = 0
	state, sig = sendCheckReplyInf("AT+CSQ\r", ok_reply)
#	print "state:"+ str(state)
#	print "sig:"+str(sig)
	if state == True:
		sig = sig.replace(',','.')
		sig_int = int(sig.split('.')[0])
		sig_dec = int(sig.split('.')[1])
		sig = float(sig)
#		print "sig_int:"+str(sig_int)
#		print "sig_dec:"+str(sig_dec)

		if (sig_int == 0) and (sig_dec == 0):
			r = -115
		elif (sig_int == 1) and (sig_dec == 0):
			r = -111
		elif (sig_int == 31) and (sig_dec == 0):
			r = -52
		elif (sig_int >= 2) and (sig_int <= 30):
			r = arduino_map(float(sig), 2, 30, -110, -54)
	return r 
#------------------TESTS-------------------------------------------
#enableGPS(True)
#print isGPSOn()
#serGPS.is_open
#flushInput();
#print sendCheckReplyInf2("AT+CGPSINFO")
#position['lat'],position['long'],position['date'],position['time'],position['alt']=getGPS()
#print position
#openSerial('/dev/ttyUSB2', 9600)
#closeSerial()
#print arduino_map(20.99, 2, 30, -110, -54)
#print getRSSI()
