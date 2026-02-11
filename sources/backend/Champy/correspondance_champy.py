import sqlite3
import os
import time
import json
from CNN_python_init import *
from neurones import *

if os.getcwd()[-3] != "m":

    os.chdir("sources/backend/Champy")

BASEDEDONNEECNNPATH = "CNN_base_de_donee.sqli"
BASEDEDONNEECORRESPONDANCEPATH = "champys_correspondance_base_de_donee.sqli"
IMAGEPATH = os.path.join(os.getcwd(),"images_tests")

def resultat_CNN(nameImg) :
    """
    Entrées :
        - <imagePath> : Le chemin vers l'image à passer dans le réseau de neurones

    Sortie :
        - <resultatMax> : La sortie prépondérante dans la liste des sorties du réseau de neurones
    """
    imagePath = os.path.join(IMAGEPATH, nameImg)
    reseauDeNeurones = init_CNN(imagePath, BASEDEDONNEECNNPATH)

    results = reseauDeNeurones.sortie()

    resultatMax = 0

    for indexResult in range(len(results)) :

        if results[indexResult] > results[resultatMax] :

            resultatMax = indexResult

    return resultatMax


def correspondance_avec_base_de_donnees(resultat) :
    """
    Entrées :
        - <resultat> : Un résultat de la fonction <resultat_CNN>

    Sortie :
        - Le nom du champignon stocké dans la base de donnée <BASEDEDONNEECORRESPONDANCEPATH>
    """
    con = sqlite3.connect("champys_correspondance_base_de_donee.sqli")
    cur = con.cursor()

    request = f"""
    SELECT nom
    FROM CHAMPY
    WHERE id = {resultat + 1}
    """

    cur.execute(request)

    return cur.fetchall()


def champy(imagePath = IMAGEPATH):

    return correspondance_avec_base_de_donnees(resultat_CNN(imagePath))[0][0]



# print(champy("3.jpg"))

#### Partie prenant en charge la liaison entre le site et l'IA, pas achevée ####
# run = True

# while run :

#     time.sleep(3)

#     with open("data.json", "r") as f :

#         data = json.load(f)

#     if data["run"] :

#         resultat = resultat_CNN(os.path.join(os.getcwd(), data["imagePath"]))
#         nomDuChampi = correspondance_avec_base_de_donnees(resultat)
#         champiDico = {"nom" : nomDuChampi}

#         with open("data2.json", "w") as f :

#             json.dump(champiDico, f)

#     if data["exit"] :

#         run = False




