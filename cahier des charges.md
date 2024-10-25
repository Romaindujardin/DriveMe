Description
Develop a Cloud Drive application (similar to Google Drive and OneDrive) using Django. To make the project simpler, the files will be stored on the server. The base folder of each user will be his login.
The tool can also work on local storage in replacement of File Explorer.
For example, if there are two users "foo" and "bar" that have uploaded some files, the file structure on the server will be simialr to this one:
•	base_server_folder
o	foo
	file1.txt
	images
	eiffel tower.png
o	bar
	bread recipe.pdf
	2024
	python lecture.pfg
Features
The web application will provide the maximum of the following features:
•	Authentication and account creation with login and password
•	Browse files and folders on a web UI
•	Display file properties and file metadata
•	Upload files
•	Create folders
•	Move and copy files and folders
•	Each account has a drive limit of 100 MB (his folder on the server cannot exceed 100 MB)
•	The max upload size is 40 MB (a file greater than 40MB cannot be uploaded)
•	The web app provides an account info screen that shows statics using graphics 
•	Example of graphic : space distribution per format (images, documents, videos, ...)
•	Preview the maximum of known formats (images, videos, pdf, source code, documents, ...)
•	Setup script to install requirements and demo data in sqlite.
•	(3+ person group) Nice, beautiful, responsive UX (demo on laptop and smartphone)
•	(4 person group) Open text, view images, play videos
Deliverable
•	A single zip file containing your source code, and at least Readme.md file explaining how the evaluator can run the project in his local computer if the setup script is not available.

Ajout supplémentaire :
•	Connexion google
•	Fonction exporter en local
•	Fichier occupant le plus de stockage
•	Corbeille
•	Partager des dossiers

