from modelioscriptor import *

def sqlType2ModelioType (t):
	types = theSession().getModel().getUmlTypes()
	if (t == "INT" or t == "BIGINT"):
		return types.getINTEGER()
	elif (t == "CHAR" or t == "VARCHAR"):
		return types.getSTRING()
	elif (t == "DATE"):
		return types.getDATE()

def doService (myp, root):
	tables = []

	for child in root.find('tables'):
		tables.append(child)

	trans = theSession().createTransaction("Class creation") 
	try:
		fact = theUMLFactory()
		dictAttribs = {}
		for table in tables:
			print "Treatment of the table '" + table.attrib.get('name') + "'."	
			PKs = []
			for pk in table.findall('primaryKey'):
				PKs.append(pk.attrib.get('column'))
			c = fact.createClass()
			c.setOwner(myp)
			c.setName(table.attrib.get('name'))
			isTable = False
			for at in table.findall('column'):
				a = fact.createAttribute(at.attrib.get('name'), sqlType2ModelioType(at.attrib.get('type')), c)
				for child in at.findall('child'):
					a.setIsDerived(True)
					if child.attrib.get('foreignKey') in dictAttribs.keys():
						dictAttribs[child.attrib.get('foreignKey')]['child'] = a
					else:
						dictAttribs[child.attrib.get('foreignKey')] = {'child': a, 'parent': None}
				if at.attrib.get('name') in PKs :
					a.addStereotype("LocalModule", "PK")
				else:
					isTable = True
				if at.find('parent') != None:
					a.addStereotype("LocalModule", "FK")
					if at.find('parent').attrib.get('foreignKey') in dictAttribs.keys():
						dictAttribs[at.find('parent').attrib.get('foreignKey')]['parent'] = a
					else:
						dictAttribs[at.find('parent').attrib.get('foreignKey')] = {'parent': a, 'child': None}
				else:
					isTable = True
			if isTable:
				c.addStereotype("LocalModule", "Table")
		for a in dictAttribs.keys():
			ass = fact.createDependency(dictAttribs[a]['parent'].getOwner(), dictAttribs[a]['child'].getOwner(), "LocalModule", "FKC")
		trans.commit()
	except:
		trans.rollback()
		raise

print "Start."

myp = None
try:
	myp = instanceNamed(Package,"MyPackage")
except:	
	print "[Error] The package named 'MyPackage' doesn't exist and need to be created."

import os
INPUT_DIRECTORY = Modelio.getInstance().getContext().getWorkspacePath().toString() + "/macros/lib/res/xmlSQL/"

tree = None
import xml.etree.ElementTree as ET
try:
	tree = ET.parse(INPUT_DIRECTORY + "library.xml")
except:
	print "[Error] The xml input file named 'library.xml' can't be found and need to be put in <$WORKSPACE/macros/lib/res/xmlSQL/>."

neededStereo = []
neededStereo.append({'name': 'PK', 'base': 'Attribute'})
neededStereo.append({'name': 'FK', 'base': 'Attribute'})
neededStereo.append({'name': 'Table', 'base': 'Class'})
neededStereo.append({'name': 'FKC', 'base': 'Dependency'})
definedStereotype = []
for p in theLocalModule().getOwnedProfile():
	for s in p.getDefinedStereotype():
		definedStereotype.append({'name': s.getName(), 'base': s.getBaseClassName()})
allStereoAvailable = True
for i in neededStereo:
	if i not in definedStereotype:
		allStereoAvailable = False
		print "[Error] The Stereotype '" + i['name'] + "' on the Meta-Class '" + i['base'] + "' doesn't exist and need to be create."		

if tree != None and myp != None and allStereoAvailable == True:
	isEmpty = True
	for o in myp.getOwnedElement(Class):
		isEmpty = False		
		o.delete()
	if isEmpty == False:
		print "[Warning] The package was not empty. All the classes in 'MyPackage' has been removed."
	doService(myp, tree.getroot())
	print "End."
else:
	print "Exit."
