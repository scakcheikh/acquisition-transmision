import xml.etree.cElementTree as ET


def packageToXML(inst, gps):
	print "Packaging . . ."
	root = ET.Element("vehicle")
	instance = ET.SubElement(root,"instance")
	date = ET.SubElement(root, "date")
	position = ET.SubElement(root, "position")

	instance.text = repr(inst)
	date.text = repr(gps['date'])
	ET.SubElement(position, "longitude").text = repr(gps['long']) 
	ET.SubElement(position, "latitude").text = repr(gps['lat']) 
	ET.SubElement(position, "altitude").text = repr(gps['alt']) 
	ET.SubElement(position, "time").text = repr(gps['time']) 
	
	filename = "./records/record_"+repr(inst)+".xml" 
	tree = ET.ElementTree(root)
	tree.write(open(filename, "w"))
	print "Xml file created !"
