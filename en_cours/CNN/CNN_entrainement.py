import sqlite3
import os
from random import *
from CNN_python_init import *
from neurones import *

os.chdir("en_cours/CNN")

IMAGEDEBUTPATH = os.path.join(os.getcwd(),"champis images/")
EXTENSIONIMAGE = ".jpg"
IMAGETESTPATH = IMAGEDEBUTPATH + "test" + EXTENSIONIMAGE
BASEDEDONNEEPATH = "CNN_base_de_donee.sqli"
LISTEDESRESULTATSPOSSIBLES = [0, 1]
COEFFICIENTSLISTE = []


def cost_CNN(reseauDeNeurones : ReseauDeNeurones, wantedResults : list) :
    """
    Entrées :
        - <reseauDeNeurones> : Un réseau de neurones
        - <wantedResults> : La liste des sorties idéales du réseau de neurones

    Sortie :
        - Le coût total du réseau de neurones, c'est à dire l'écart entre l'idéal et la réalité des sorties
    """
    results = reseauDeNeurones.sortie()

    assert len(results) == len(wantedResults)

    cost = 0

    for indexResult in range(len(results)) :

        cost += (wantedResults[indexResult] - results[indexResult]) ** 2

    return cost



def derivee_partielle_cost(reseauDeNeurones : ReseauDeNeurones, wantedResults : list, indiceCoefADeriver : int, indiceNeuroneCoefADeriver : int, indiceCoucheCoefADeriver : int) :
    """
    Entrées :
        - <reseauDeNeurones> : Un réseau de neurones
        - <wantedResults> : La liste des sorties idéales du réseau de neurones
        - <indiceCoefADeriver> : L'indice du coefficient pour lequel nous allons effectuer la dérivée partielle
        - <indiceNeuroneCoefADeriver> : L'indice du neurone dans lequel se trouve le coefficient à dériver
        - <indiceCoucheCoefADeriver> : L'indice de la couche dans laquelle est le neurone dans lequel se trouve le coefficient à dériver

    Sortie :
        - La dérivée partielle du coût en fonction d'un coefficient, c'est à dire les modifications à apporter sur le coefficient permettant de réduire le coût du réseau de neuronnes 
    """
    results = reseauDeNeurones.sortie()
    resultsDerivees = reseauDeNeurones.derivee_partielle(indiceCoefADeriver, indiceNeuroneCoefADeriver, indiceCoucheCoefADeriver)

    assert len(results) == len(wantedResults)

    costDerive = 0

    for indexResult in range(len(results)) :

        costDerive += 2 * ((wantedResults[indexResult] - results[indexResult]) * (- resultsDerivees[indexResult]))

    return costDerive



def derivee_partielle_cost_moyen(coefficients , indiceCoefADeriver : int, indiceNeuroneCoefADeriver : int, indiceCoucheCoefADeriver : int) :
    """
    Entrées :
        - <coefficients> : La liste des coefficients représentant les réseaux de neuronnes
        - <indiceCoefADeriver> : L'indice du coefficient pour lequel nous allons effectuer la dérivée partielle
        - <indiceNeuroneCoefADeriver> : L'indice du neurone dans lequel se trouve le coefficient à dériver
        - <indiceCoucheCoefADeriver> : L'indice de la couche dans laquelle est le neurone dans lequel se trouve le coefficient à dériver

    Sortie :
        - La dérivée partielle du coût moyen en fonction d'un coefficient, c'est à dire les modifications à apporter sur le coefficient permettant de réduire le coût du réseau de neuronnes 
    """
    nbSorties = len(LISTEDESRESULTATSPOSSIBLES)

    if coefficients == None :

        baseDeDonnePath = BASEDEDONNEEPATH

    else :

        baseDeDonnePath = None

    costsDerivesMoy = 0

    imagePath = f"{IMAGEDEBUTPATH}{0}{EXTENSIONIMAGE}"
    reseauDeNeurone = init_CNN(imagePath, baseDeDonnePath, coefficients)

    for indiceReseau in range(0, nbSorties) :

        imagePath = f"{IMAGEDEBUTPATH}{indiceReseau}{EXTENSIONIMAGE}"
        reseauDeNeurone.changer_inputs_image(imagePath)
        wantedResults = create_wanted_results(indiceReseau)
        costDerive = derivee_partielle_cost(reseauDeNeurone, wantedResults, indiceCoefADeriver, indiceNeuroneCoefADeriver, indiceCoucheCoefADeriver)
        costsDerivesMoy += costDerive

    costsDerivesMoy /= nbSorties

    return costsDerivesMoy



def descente_de_gradient(learningRate, coefficients = None) :
    """
    Entrées :
        - <learningRate> : Le taux sur la modification des coefficients (plus il est élevé plus ce sera agressif, plus il est bas, plus ce sera précis)
        - <coefficients> : La liste des coefficients représentant les réseaux de neuronnes

    Sortie :
        - Modifie les coefficients permettant de réduire le coût moyen du réseau de neuronnes 
    """
    imagePath = IMAGETESTPATH

    if coefficients == None :

        baseDeDonnePath = BASEDEDONNEEPATH

    else :

        baseDeDonnePath = None

    reseauDeNeurone = init_CNN(imagePath, baseDeDonnePath, coefficients)
    nouveauxCoefficients = []

    if coefficients == None :

        coefficients = reseauDeNeurone.coefficients()

    for couche in range(len(coefficients)) :

        nouveauxCoefficients.append([])

        print(couche)

        for indiceNeurone in range(len(coefficients[couche])) :

            nouveauxCoefficients[couche].append([])

            for indiceCoef in range(len(coefficients[couche][indiceNeurone])) :

                ancienCoefTemp = coefficients[couche][indiceNeurone][indiceCoef]
                deriveePartielleCostMoyenTemp = derivee_partielle_cost_moyen(coefficients, indiceCoef, indiceNeurone, couche)
                nouveauxCoefficients[couche][indiceNeurone].append(ancienCoefTemp - learningRate * deriveePartielleCostMoyenTemp)

    return nouveauxCoefficients



def create_wanted_results(resultatVoulu : int) :
    """
    Entrée :
        - <resultatVoulu> : un entier correspondant à l'indice du résultat voulu (par rapport aux sorties du réseau de neurones)

    Sortie :
        - Une liste de la longueur de la liste de sortie du réseau de neurones actuellement pris en charge par ce programme d'entraînement avec tout à 0 sauf celui d'indice <resultatVoulu> égal à 1
    """
    assert resultatVoulu in LISTEDESRESULTATSPOSSIBLES
    
    wantedResults = []

    for index in range(len(LISTEDESRESULTATSPOSSIBLES)) :

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
    nbSorties = len(LISTEDESRESULTATSPOSSIBLES)

    if coefficients == None :

        baseDeDonnePath = BASEDEDONNEEPATH

    else :

        baseDeDonnePath = None

    costsMoy = 0
    imagePath = f"{IMAGEDEBUTPATH}{0}{EXTENSIONIMAGE}"
    reseauDeNeurone = init_CNN(imagePath, baseDeDonnePath, coefficients)
    

    for indiceReseau in range(0, nbSorties) :

        imagePath = f"{IMAGEDEBUTPATH}{indiceReseau}{EXTENSIONIMAGE}"
        reseauDeNeurone.changer_inputs_image(imagePath)
        wantedResults = create_wanted_results(indiceReseau)
        costTemp = cost_CNN(reseauDeNeurone, wantedResults)
        costsMoy += costTemp

    costsMoy /= nbSorties

    return costsMoy



def sauvegarde_coefficients(listeDesCoefficients, listeDesBiais = [[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0]]) :
    """
    Entrées : 
        - <listeDesCoefficients> : La liste des coefficients du réseau à sauvegarder
        - <listeDesBiais> : La liste des biais à sauvegarder

    Action :
        - Enregistre les coefficients et les biais dans la base de donnée
    """
    con = sqlite3.connect(BASEDEDONNEEPATH)
    cur=con.cursor()

    nbCouches = len(listeDesCoefficients)

    for couche in range(nbCouches) :

        for neurone in range(len(listeDesBiais[couche])) :

            request = f""" 
            UPDATE COUCHES{couche}
            SET biais = {listeDesBiais[couche][neurone]}
            WHERE neurones = {neurone}
            """

            cur.execute(request)

            for coefficient in range(len(listeDesCoefficients[couche][neurone])) :

                request = f"""
                UPDATE COUCHE{couche}NEURONE{neurone}
                SET coefficient = {listeDesCoefficients[couche][neurone][coefficient]}
                WHERE ID = {coefficient + 1}
                """

                cur.execute(request)


    con.commit()
    con.close()



def training(nbTours, explore = False) :
    """
    Entrée :
        - <nbTours> : Le nombre de tours d'entraînement qui vont être effectués

    Action : 
        - Créer plusieurs variantes du réseau de neurones principal
        - Sauvegarder le plus efficient par rapport à son coût moyen
    """
    while nbTours >= 0 :
    
        print(nbTours,":")

        imagePath = IMAGEDEBUTPATH + "1" + EXTENSIONIMAGE
        listeDeReseauxDeNeurones = []
        listeDeReseauxDeNeurones.append(init_CNN(imagePath, BASEDEDONNEEPATH))

        indiceMin = 0
        cost_moyen_min = calcul_cost_moyen(listeDeReseauxDeNeurones[indiceMin].coefficients())

        if  explore :

            for _ in range(1, 101) :

                structureNeuronaleTemporaire = init_CNN(imagePath, BASEDEDONNEEPATH)
                structureNeuronaleTemporaire.changer_coefs_randomly()
                listeDeReseauxDeNeurones.append(structureNeuronaleTemporaire)

                cost_moyen_a_tester = calcul_cost_moyen(structureNeuronaleTemporaire.coefficients())

                if cost_moyen_a_tester <= cost_moyen_min :

                    indiceMin = len(listeDeReseauxDeNeurones) - 1
                    cost_moyen_min = cost_moyen_a_tester
                    print("Trouvé !!!")
                
                if cost_moyen_a_tester <= cost_moyen_min :

                    print("Trouvé !")
                    print(cost_moyen_a_tester)

                    for learningRate in range(1, 10) : 

                        indiceReseauAAmeliorer = len(listeDeReseauxDeNeurones) - 1
                        structureNeuronaleTemporaire = init_CNN(imagePath, None, listeDeReseauxDeNeurones[indiceReseauAAmeliorer].coefficients())
                        structureNeuronaleTemporaire.changer_coefs(descente_de_gradient(5 / learningRate, structureNeuronaleTemporaire.coefficients()))
                        listeDeReseauxDeNeurones.append(structureNeuronaleTemporaire)

                        cost_moyen_a_tester = calcul_cost_moyen(structureNeuronaleTemporaire.coefficients())
                        print(cost_moyen_a_tester)
                        if cost_moyen_a_tester <= cost_moyen_min :

                            indiceMin = len(listeDeReseauxDeNeurones) - 1
                            cost_moyen_min = cost_moyen_a_tester
                            print("Trouvé !!!")

        else :

            for learningRate in range(1, 10) : 

                indiceReseauAAmeliorer = len(listeDeReseauxDeNeurones) - 1
                structureNeuronaleTemporaire = init_CNN(imagePath, None, listeDeReseauxDeNeurones[indiceReseauAAmeliorer].coefficients())
                structureNeuronaleTemporaire.changer_coefs(descente_de_gradient(5 / learningRate, structureNeuronaleTemporaire.coefficients()))
                listeDeReseauxDeNeurones.append(structureNeuronaleTemporaire)

                cost_moyen_a_tester = calcul_cost_moyen(structureNeuronaleTemporaire.coefficients())
                print(cost_moyen_a_tester)
                if cost_moyen_a_tester <= cost_moyen_min :

                    indiceMin = len(listeDeReseauxDeNeurones) - 1
                    cost_moyen_min = cost_moyen_a_tester
                    print("Trouvé !!!")


        sauvegarde_coefficients(listeDeReseauxDeNeurones[indiceMin].coefficients())

        imagePath = 0
        listeDeReseauxDeNeurones = []
        cost_moyen_a_tester = 0
        indiceMin = 0
        cost_moyen_min = 0
        structureNeuronaleTemporaire = 0

        print(calcul_cost_moyen(),"\n")

        nbTours -= 1

training(10000000, False)
print(calcul_cost_moyen())