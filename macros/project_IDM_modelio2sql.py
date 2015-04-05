def umlBasicType2sql(basicType):
	t = basicType.name
	if (t == "string"):	
		return "VARCHAR"
	elif (t == "integer"):	
		return "INT"
	elif (t == "date"):	
		return "DATE"
	else:
		return t

def umlClass2sql(umlClass):
	print "CREATE TABLE " + umlClass.name + " ("
	pk_list = []
	fk_list = []
	for a in umlClass.ownedAttribute:
		st = a.getExtension()
		for s in st:
			if (s.name == "PK"):
				pk_list.append(a.name)
			elif (s.name == "FK"):
				fk_ref_string = a.getDependsOnDependency()[0].getDependsOn().getOwner().name + "(" + a.getDependsOnDependency()[0].getDependsOn().name + ")"
				fk_string = "\tCONSTRAINT fk_" + umlClass.name + "_" + a.name + " FOREIGN KEY (" + a.name + ") REFERENCES " + fk_ref_string
				fk_list.append(fk_string)
	for a in umlClass.ownedAttribute:
		print "\t" + a.name + " " + umlBasicType2sql(a.type) + ","
	pk_string = "\tCONSTRAINT pk_" + umlClass.name + " PRIMARY KEY (" + ", ".join(pk_list) + ")"
	if (len(fk_list) > 0):
		pk_string += ","
	print pk_string
	print ",\n".join(fk_list)
	print ");\n"

def associationsInPackage(package):
	toReturn = []
	for e in package.getOwnedElement():
		if isinstance(e, Class):
			for t in e.targetingEnd:
				if t.association not in toReturn and t.association.getLinkToClass() == None:
					toReturn.append(t.association)
	return toReturn

def package2sql(package):
	for e in package.getOwnedElement():
		if isinstance(e, Class):
			umlClass2sql(e)
	
print "Start."
no_select_error = "[Error] The package named 'PackageScribeSQL' which contains all classes isn't selected."
if (len(selectedElements) == 0):
	print no_select_error
	print "Exit."
elif (not isinstance(selectedElements[0], Package) or selectedElements[0].name != "PackageScribeSQL"):
	print no_select_error
	print "Exit."	
else:
	print "Output :\n------------\n\n"
	package2sql(selectedElements[0])
	print "\n------------\nEnd."
	