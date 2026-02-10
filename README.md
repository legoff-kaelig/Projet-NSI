# 📘 MANUEL D'UTILISATION
## Projet Trophées NSI 2026 - Application météo et de reconnaissance d'images
---
### Application météo :
1. Installer le module `requests` en tapant `py -m pip install requests` dans la console. 
2. Lancer le script `init.py` dans le dossier `sources/backend`.
3. Ouvrir la page `home.html` qui se trouve dans le dossier `sources/frontend` puis autoriser la géolocalisation. En cas de refus, celle-ci se fera automatiquement à Paris.
4. Activer DevTools (`F12` ou Menu Déroulant) puis activer la vue en format téléphone.
---
### Reconnaissance d'images :
1. Installer le module `pillow` en tapant `py -m pip install pillow` dans la console. 
2. Lancer le script `run_champy.py` dans le dossier `sources/backend/Champy`.
3. Téléverser une image de test de champignon se situant dans le dossier `sources/backend/Champy/Images_tests` dans l'emplacement prévu à cet effet sur la page `scan.html`. Celle-ci est accessible directement depuis la page `home.html` depuis la barre de navigation.
4. Appuyer sur valider pour recevoir le nom de ce champignon.