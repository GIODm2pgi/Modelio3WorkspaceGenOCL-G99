#
# CoExplorer
#
# Model/Metamodel co-explorer for Modelio.
#
# Author: jmfavre
#
# Compatibility: Modelio 2.x, Modelio 3.x
#
# Target audience:
#   This script mainly dedicated to developers who need to understand modelio Metamodel,
#   for instance to develop scripts or modules. It allows the co-exploration of a model
#   and the corresponding metamodel.
#
# Description:
#   This macro allows to explore the set of selected elements by navigating at the
#   same time in the model and the metamodel. While Modelio' model explorer and property
#   sheets presents a "user oriented" view of the model, the CoExplorer will present
#   a view strictly in line with the actual metamodel. 
#   The set of all (non empty) features associated with each element is displayed,
#   allowing the navigation to continue. Note that the tree is virtually infinite and
#   that there is currently no indication that an element has been already visited.
#   The methods followed are those of the form getXXX(), isXXX() and toString() with no
#   parameters. A few "virtual" methods which do not have direct correspondance in modelio
#   are also added, in particular to enable navigation to and within diagrams.
#   The co-explorer allows to navigate at the same time the model
#   and discover a slice of the metamodel, the slice that is useful for the model at hand.
#   The explorer not only allow to explore ModelElement, but also other Java entities,
#   and interestingly enough the DiagramGraphic elements. In modelio graphical entities
#   are not modeled, but the exploration is made possible.
#
# Installation:
#   This script should be installed as a workspace macro using standard modelio procedure
#   to add macros. The options to use are the following options:
#      - "Applicable on" : No Selection. The macro is application on any kind of element
#      - "Show in contextual menu" : YES
#      - "Show in toolbar" : YES
#   This script is based on the content of the "lib" directory which must be copied manually
#   in the same directory as this very file. That is, in the directory where this file
#   CoExplorer.py will be installed by modelio through the standard macro installation procedure.
#   Ultimately we should have the following structure 
#          CoExplorer.py             <--- this very file
#             lib/
#                 introspection.py
#                 misc.py
#                 modelioscriptor.py
#                 ...                <--- possibly other jython modules
#                 res/
#                     assoc-1.gif
#                     assoc-n.gif
#                     ...            <--- other resources.
#
# History
#   Version 1.1 - December 02, 2013
#      - addition of some explaination on startup
#      - use modelioscriptor
#      - changes in startup 
#   Version 1.0 - October 31, 2013
#      - first public realease

# MODULES_TO_RELOAD = []
MODULES_TO_RELOAD = ["modelioscriptor"]

def startup():
  print "The CoExplorer is starting ..."

  #---- add the "lib" directory to the path
  # The code below compute this path and put it in the variable SCRIPT_LIBRARY_DIRECTORY. 
  # Feel free to change it if necessary. Currently the "lib" directory is search within
  # the directory of this very file, but if you may want to change its location you can
  # uncomment the line defining SCRIPT_LIBRARY_DIRECTORY with an absolute path
  try:
    from org.modelio.api.modelio import Modelio
    orgVersion = True
  except:
    orgVersion = False
  import os
  import sys 
  WORKSPACE_DIRECTORY=Modelio.getInstance().getContext().getWorkspacePath().toString()
  if orgVersion:
    MACROS_DIRECTORY=os.path.join(WORKSPACE_DIRECTORY,'macros')
  else:
    MACROS_DIRECTORY=os.path.join(WORKSPACE_DIRECTORY,'.config','macros')
  SCRIPT_LIBRARY_DIRECTORY=os.path.join(MACROS_DIRECTORY,'lib')
  # Uncomment this line and adjust it if you want to put the "lib" directory somewhere else
  # SCRIPT_LIBRARY_DIRECTORY = "C:\\MODELIO3-WORKSPACE\\macros\\lib"
  sys.path.extend([MACROS_DIRECTORY,SCRIPT_LIBRARY_DIRECTORY])
  #print "   Current workspace is "+WORKSPACE_DIRECTORY
  #print "   "+MACROS_DIRECTORY+" added to script path"
  #print "   "+SCRIPT_LIBRARY_DIRECTORY+" added to script path"

  
#---- check if this is the first time this macro is loaded or not  
try:
  CO_EXPLORER_EXECUTION += 1
  # this is the not the first time
except:
  # this is the first time
  CO_EXPLORER_EXECUTION = 1
  startup()
    

if "modelioscriptor" in MODULES_TO_RELOAD:
  try: del sys.modules["modelioscriptor"] ; del modelioscriptor
  except: pass
from modelioscriptor import *


#######################################################"

# TODO : delete le contenu du package

def sqlType2ModelioType (t):
	types = theSession().getModel().getUmlTypes()
	if (t == "INT" or t == "BIGINT"):
		return types.getINTEGER()
	elif (t == "CHAR" or t == "VARCHAR"):
		return types.getSTRING()
	elif (t == "DATE"):
		return types.getDATE()

import xml.etree.ElementTree as ET
tree = ET.parse('library.xml')
root = tree.getroot()

tables = []

for child in root.find('tables'):
	tables.append(child)

trans = theSession().createTransaction("Class creation") 
try:
	fact = theUMLFactory()
	myp = instanceNamed(Package,"MyPackage")
	dictAttribs = {}
	for table in tables:	
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

print "FIN"
