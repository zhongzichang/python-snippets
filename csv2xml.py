#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import csv
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

#usage:  python csv2xml.py heroes.csv 
# will gen heroes.xml and heroes.cs

def gen_csharp(csv_name, src_file):
	src = """
using System.Xml;
using UnityEngine;

namespace TangGame.Xml
{
	public class HeroXml
	{ 
%s 
	}
}"""
	members = []

	csvfile = open(csv_name, 'rU')
	# reader = csv.DictReader( csvfile, delimiter=";", quoting=csv.QUOTE_NONE)
	reader = csv.DictReader( csvfile, delimiter=",", quoting=csv.QUOTE_ALL)
	# print reader.fieldnames

	row = list(reader) [2]
	# print row
	for col in reader.fieldnames:
		# val = row[col].decode("gbk")
		val = row[col].decode("gbk",'ignore')
		
		if re.match(r"^\d+$", val):
			members += ["\t\tpublic int " + col]
		else:
			members += ["\t\tpublic string " + col]
	allmembers = ";\r\n".join(members)
	open(src_file, "w").write(src % (allmembers))

def gen_xml(csv_name, xml_file):
	csvfile = open(csv_name, 'rU')
	# reader = csv.DictReader( csvfile, delimiter=";", quoting=csv.QUOTE_NONE)
	reader = csv.DictReader( csvfile, delimiter=",", quoting=csv.QUOTE_ALL)
	# print reader.fieldnames

	root = ET.Element('root')
        rowIndex = 0
	for row in reader:
                rowIndex+=1
                if (rowIndex == 1):
                        continue
		node = ET.SubElement(root, 'value')
		for col in reader.fieldnames:
			# val = row[col].decode("gbk")
			val = row[col].decode("gbk",'ignore')
			
			if val:
				lvNode = ET.SubElement(node, col)
				lvNode.text = val
	rough_string = ET.tostring(root, encoding='utf-8')
	reparsed = minidom.parseString(rough_string)
	text = reparsed.toprettyxml(indent=" " , encoding="utf-8")
	open(xml_file, "w").write(text)

if __name__ == '__main__':

	reload(sys) 
	sys.setdefaultencoding('utf-8')

	csv_name = sys.argv[1]
	src_file = csv_name.replace(".csv", ".cs")
	xml_file = csv_name.replace(".csv", ".xml")
	# print csv_name
	gen_csharp(csv_name, src_file)
	gen_xml(csv_name, xml_file)
