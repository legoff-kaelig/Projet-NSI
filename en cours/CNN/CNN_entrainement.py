import sqlite3
from random import *
from CNN_python_init import *
from neurones import *

imagePath = "C:/Users/Riwan/Documents/GitHub/Projet-NSI/en cours/CNN/nombres écrits à la main pour entrainer un modèle basique de reconnaissance d'image/7.png"
baseDeDonneePath = "CNN_base_de_donee.sqli"
listeDesResultatsPossibles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



def cost_CNN(reseauDeNeurones : ReseauDeNeurones, wantedResults : list) :

    results = reseauDeNeurones.sortie()

    assert len(results) == len(wantedResults)

    cost = 0

    for indexResult in range(len(results)) :

        cost += (wantedResults[indexResult] - results[indexResult]) ** 2

    return cost



def create_wanted_results(resultatVoulu : int) :

    assert resultatVoulu in listeDesResultatsPossibles
    
    wantedResults = []

    for index in range(len(listeDesResultatsPossibles)) :

        if index == resultatVoulu :

            wantedResults.append(1)

        else :

            wantedResults.append(0)

    return wantedResults


reseauDeNeurone = init_CNN(imagePath, baseDeDonneePath)
resultatVoulu = 7
wantedResults = create_wanted_results(resultatVoulu)

print(cost_CNN(reseauDeNeurone, wantedResults))