import xml.etree.cElementTree as ET

import packageToXML 

inst = 1
date ="23/12/2016"
position = {'longitude':12.33456, 'latitude':3.4565, 'altitude':134, 'time':'12:34:05'}

if __name__ == '__main__':
	packageToXML.packageToXML(inst, date, position)
