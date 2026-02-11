# 📘 MANUEL D'UTILISATION
## Projet Trophées NSI 2026 - Application météo et de reconnaissance d'images
---
### Modules à installer :
1. Installer le module `pillow` en tapant `py -m pip install pillow` dans la console.
2. Installer le module `flask` en tapant `py -m pip install flask` dans la console.
3. Installer le module `requests` en tapant `py -m pip install requests` dans la console.
4. Installer le module `flask_cors` en tapant `py -m pip install flask_cors` dans la console.

---

### Fichiers à exécuter parallèlement :

1. Lancer le script `run.py` dans le dossier `sources/backend/Champy`.
2. Lancer le script `init.py` dans le dossier `sources/backend` sur un autre terminal.

---
### Site web :

##### Page météo :

1. Ouvrir la page `home.html` qui se trouve dans le dossier `sources/frontend` puis autoriser la géolocalisation. En cas de refus, celle-ci se fera automatiquement à Paris.
2. Activer DevTools (`F12` ou Menu Déroulant) puis activer la vue en format téléphone.

##### Page reconnaissance de champignons :

3. Aller sur la page `scan.html` qui se trouve dans le dossier `sources/frontend` et est accessible par la page `home.html` ouverte précédement en cliquant sur le menu en bas de celle-ci.
4. Cliquer sur `Parcourir les fichiers` puis choisir l'image de champignon à tester, ayant besoin d'un format spécifique des images dédiées au test sont situées dans le dossier `backend/Champy/Images_tests`.
5. Regarder le nom du champignon s'afficher sous l'image de ce dernier.

---

### Suivi des tâches
[Cliquer-ici pour accéder à la feuille de suivi des tâches](https://docs.google.com/spreadsheets/d/1xPUP9ya7HwvEknu5ojBkGyNHl8VxsbrCi78x2pxM2xc/edit?usp=sharing)