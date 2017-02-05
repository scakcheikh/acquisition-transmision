#!/usr/bin/env python
#

import sys
from subprocess import call

#Elligible wireless SSIDs
wlans = ["scakworld", "AndroidAP2"]

# You can add or change the functions to parse the properties of each AP (cell)
# below. They take one argument, the bunch of text describing one cell in iwlist
# scan and return a property of that cell.

def get_name(cell):
    return matching_line(cell,"ESSID:")[1:-1]
def get_signal(cell):
    signal = matching_line(cell, "Quality=").split("level=")[1].split("dBm")[0]
    return int(signal)


# Utils functions

def matching_line(lines, keyword):
    """Returns the first matching line in a list of lines. See match()"""
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching
    return None

def match(line,keyword):
    """If the first part of line (modulo blanks) matches keyword,
    returns the end of that line. Otherwise returns None"""
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        return None

def wifiSignal(STDIN, linkDictionnary):
    cells=[[]]

    for line in STDIN:
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())
    cells=cells[1:]
    
    for cell in cells:
	wlanName = get_name(cell) 
	if (wlanName in wlans):
	    linkDictionnary.update({wlanName:get_signal(cell)})	
	    #print wlanName+':'+get_signal(cell)+ "dBm"

