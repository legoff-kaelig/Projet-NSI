# 📘 MANUEL D'UTILISATION
## Projet Trophées NSI 2026 - Application météo et de reconnaissance d'images
---
### Application météo :
###### Le projet contient deux pages HTML distinctes dans le dossier frontend qui sont `home.html` et `scan.html` ; cependant `scan.html` n'est pas tout à fait fonctionnelle car celle-ci n'est pas encore reliée au backend en raison d'un manque de temps.
1. Installer le module `requests` en tapant `py -m pip install requests` dans la console. 
2. Lancer le script `init.py` dans le dossier `sources/backend`.
3. Ouvrir la page `home.html` qui se trouve dans le dossier `sources/frontend` puis autoriser la géolocalisation. En cas de refus, celle-ci se fera automatiquement à Paris.
4. Activer DevTools (`F12` ou Menu Déroulant) puis activer la vue en format téléphone.
---
### Reconnaissance d'images :
1. Installer le module `pillow` en tapant `py -m pip install pillow` dans la console. 
2. Lancer le script `run_champy.py` dans le dossier `sources/backend/Champy`.
3. Exécuter la fonction `champy()` avec en argument le chemin d'accès vers l'image à tester, ayant besoin d'un format spécifique des images dédiées au test, situées dans le dossier `backend/Champy/Images_tests`
---
### Suivi des tâches
[Cliquer-ici pour accéder à la feuille de suivi des tâches](https://docs.google.com/spreadsheets/d/1xPUP9ya7HwvEknu5ojBkGyNHl8VxsbrCi78x2pxM2xc/edit?usp=sharing)