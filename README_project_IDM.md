PROJET IDM M2PGI : SQLSCRIBE
===========================

XML -> MODELIO
---------------

Le script est nommé **project_IDM_xml2modelio**. Le fichier source est **macros/project_IDM_xml2modelio.py**. 

Les pré-requis sont :

	* Un projet doit être ouvert et sélectionné.
	
	* Un package nommé "PackageScribeSQL" doit existé.
	
	* Les stéréotypes "PK" (Attribute), "FK" (Attribute), "FKC" (Dependency) et "Table" (Class) doivent existés.
	
	* Un fichier **bdd.xml** doit se trouver dans le répertoire **lib/res/xml/**
	
Attention, si le package "PackageScribeSQL" n'est pas vide au lancement du script, le contenu sera supprimé !

Le résultat se trouve dans le package "PackageScribeSQL".

Remarque : pour afficher les liens des clés étrangères (foreign key) sur le diagramme, il faire **Unmask -> Non structuring link**.

MODELIO -> SQL
---------------

Le script est nommé **project_IDM_modelio2sql**. Le fichier source est **macros/project_IDM_modelio2sql.py**. 

Les pré-requis sont :

	* Un projet doit être ouvert et sélectionné.
	
	* Un package nommé "PackageScribeSQL" doit existé et être sélectionné.
	
	* Le format du contenu du package "PackageScribeSQL" doit correspondre au format généré par le script **project_IDM_xml2modelio** : une table = une classe, stereotype "PK" sur les clés primaires, stéréotype "FK" sur les clés étrangères, utilisation des "dependency" etc ...
	
Le résultat est directement afficher dans la console.
	
