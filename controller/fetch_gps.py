#!/usr/bin/env python


import time
import serial


ser = serial.Serial(
   port='/dev/ttyACM0',
   baudrate = 115200,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)

x =""
i = 0
coordinate =""
while 1:
  x=str(ser.readline())
  print x
  if len(x) >= 4 and x[0] == "l" and x[1] == "i" and x[2] == "s" and x[3] == "t":
    if i == 1:
      time.sleep(5)
    if i == 0:
      i=1
    ser.write('g')
  if len(x) >= 4 and x[0] == "l" and x[1] == "a" and x[2] == "t" and x[3] == ":":
    coordinate = x
    print "Coordinate --->: ", coordinate

    