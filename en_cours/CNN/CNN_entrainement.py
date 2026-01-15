import sqlite3
import os
from random import *
from CNN_python_init import *
from neurones import *

os.chdir("en_cours/CNN")

IMAGEDEBUTPATH = os.path.join(os.getcwd(),"nombres écrits à la main pour entrainer un modèle basique de reconnaissance d'image/")
IMAGEFINPATH = ".png"
BASEDEDONNEEPATH = "CNN_base_de_donee.sqli"
LISTEDESRESULTATSPOSIBLES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
COEFFICIENTSLISTE = []



def cost_CNN(reseauDeNeurones : ReseauDeNeurones, wantedResults : list) :
    """
    Entrées :
        - <reseauDeNeurones> : Un réseau de neurones
        - <wantedResults> : la liste des sorties idéales du réseau de neurones

    Sorite :
        - Le coût total du réseau de neurones, c'est à dire l'écart entre l'idéal et la réalité des sorties
    """
    results = reseauDeNeurones.sortie()

    assert len(results) == len(wantedResults)

    cost = 0

    for indexResult in range(len(results)) :

        cost += (wantedResults[indexResult] - results[indexResult]) ** 2

    return cost



def create_wanted_results(resultatVoulu : int) :
    """
    Entrée :
        - <resultatVoulu> : un entier correspondant à l'indice du résultat voulu (par rapport aux sorties du réseau de neurones)

    Sortie :
        - Une liste de la longueur de la liste de sortie du réseau de neurones actuellement pris en charge par ce programme d'entraînement avec tout à 0 sauf celui d'indice <resultatVoulu> égal à 1
    """
    assert resultatVoulu in LISTEDESRESULTATSPOSIBLES
    
    wantedResults = []

    for index in range(len(LISTEDESRESULTATSPOSIBLES)) :

        if index == resultatVoulu :

            wantedResults.append(1)

        else :

            wantedResults.append(0)

    return wantedResults



def calcul_cost_moyen(coefficients = None) :
    """
    Entrée :
        - <coefficients> : la liste des coefficients testés, si None, la base de donnée du fichier d'entraînement (celui-ci) est utilisé

    Sortie :
        - Le coût moyen de ce modèle pour toutes les sorties possibles par rapport à des datas d'entraînement
    """
    reseauxDeNeurones = []
    nbSorties = len(LISTEDESRESULTATSPOSIBLES)

    if coefficients == None :

        baseDeDonnePath = BASEDEDONNEEPATH

    else :

        baseDeDonnePath = None

    costsMoy = 0

    for indiceReseau in range(nbSorties) :

        imagePath = f"{IMAGEDEBUTPATH}{indiceReseau}{IMAGEFINPATH}"
        reseauDeNeurone = init_CNN(imagePath, baseDeDonnePath, coefficients)
        reseauxDeNeurones.append(reseauDeNeurone)
        resultatVoulu = indiceReseau
        wantedResults = create_wanted_results(resultatVoulu)
        cost = cost_CNN(reseauxDeNeurones[indiceReseau], wantedResults)
        costsMoy += cost

    costsMoy /= nbSorties

    return costsMoy

print(calcul_cost_moyen())