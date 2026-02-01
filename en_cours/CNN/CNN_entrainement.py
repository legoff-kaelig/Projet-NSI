import sqlite3
import os
from random import *
from CNN_python_init import *
from neurones import *

os.chdir("en_cours/CNN")

IMAGEDEBUTPATH = os.path.join(os.getcwd(),"nombres écrits à la main pour entrainer un modèle basique de reconnaissance d'image/")
IMAGEFINPATH = ".png"
IMAGETESTPATH = IMAGEDEBUTPATH + "test" + IMAGEFINPATH
BASEDEDONNEEPATH = "CNN_base_de_donee.sqli"
LISTEDESRESULTATSPOSSIBLES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
COEFFICIENTSLISTE = []


def cost_CNN(reseauDeNeurones : ReseauDeNeurones, wantedResults : list) :
    """
    Entrées :
        - <reseauDeNeurones> : Un réseau de neurones
        - <wantedResults> : la liste des sorties idéales du réseau de neurones

    Sortie :
        - Le coût total du réseau de neurones, c'est à dire l'écart entre l'idéal et la réalité des sorties
    """
    results = reseauDeNeurones.sortie()

    assert len(results) == len(wantedResults)

    cost = 0

    for indexResult in range(len(results)) :

        cost += (wantedResults[indexResult] - results[indexResult]) ** 2

    return cost



def derivee_partielle_cost(reseauDeNeurones : ReseauDeNeurones, wantedResults : list, indiceCoefADeriver : int, indiceNeuroneCoefADeriver, indiceCoucheCoefADeriver : int) :

    results = reseauDeNeurones.sortie()
    resultsDerivees = reseauDeNeurones.derivee_partielle(indiceCoefADeriver, indiceNeuroneCoefADeriver, indiceCoucheCoefADeriver)

    assert len(results) == len(wantedResults)

    costDerive = 0

    for indexResult in range(len(results)) :

        costDerive += 2 * ((wantedResults[indexResult] - results[indexResult]) * (- resultsDerivees[indexResult]))

    return costDerive



def derivee_partielle_cost_moyen(coefficients , indiceCoefADeriver : int, indiceNeuroneCoefADeriver : int, indiceCoucheCoefADeriver : int) :
    
    reseauxDeNeurones = []
    nbSorties = len(LISTEDESRESULTATSPOSSIBLES)

    if coefficients == None :

        baseDeDonnePath = BASEDEDONNEEPATH

    else :

        baseDeDonnePath = None

    costsDerivesMoy = 0

    for indiceReseau in range(nbSorties) :

        imagePath = f"{IMAGEDEBUTPATH}{indiceReseau}{IMAGEFINPATH}"
        reseauDeNeurone = init_CNN(imagePath, baseDeDonnePath, coefficients)
        reseauxDeNeurones.append(reseauDeNeurone)
        resultatVoulu = indiceReseau
        wantedResults = create_wanted_results(resultatVoulu)
        costDerive = derivee_partielle_cost(reseauxDeNeurones[indiceReseau], wantedResults, indiceCoefADeriver, indiceNeuroneCoefADeriver, indiceCoucheCoefADeriver)
        costsDerivesMoy += costDerive

    costsDerivesMoy /= nbSorties

    return costsDerivesMoy



def descente_de_gradient(learningRate, coefficients = None) :

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

        for indiceNeurone in range(len(coefficients[couche])) :

            for indiceCoef in range(len(coefficients[indiceNeurone])) :

                nouveauxCoefficients.append(coefficients[couche][indiceNeurone][indiceCoef] - learningRate * (derivee_partielle_cost_moyen(coefficients, indiceCoef, indiceNeurone, couche)))

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
    reseauxDeNeurones = []
    nbSorties = len(LISTEDESRESULTATSPOSSIBLES)

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



def sauvegarde_coefficients(listeDesCoefficients, listeDesBiais = [[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]) :
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



def calcul_cost_moyen_liste_de_reseaux(listeDeReseauxDeNeurones):

    indiceMin = 0
    cost_moyen_min = calcul_cost_moyen(listeDeReseauxDeNeurones[indiceMin].coefficients())

    for structureNeuronaleIndice in range(1, len(listeDeReseauxDeNeurones)) :
        
        cost_moyen_a_tester = calcul_cost_moyen(listeDeReseauxDeNeurones[structureNeuronaleIndice].coefficients())

        if cost_moyen_a_tester <= cost_moyen_min :

            indiceMin = structureNeuronaleIndice
            cost_moyen_min = cost_moyen_a_tester

    return listeDeReseauxDeNeurones[indiceMin].coefficients()



def training(nbTours) :
    """
    Entrée :
        - <nbTours> : Le nombre de tours d'entraînement qui vont être effectués

    Action : 
        - Créer plusieurs variantes du réseau de neurones principal
        - Sauvegarder le plus efficient par rapport à son coût moyen
    """
    if nbTours <= 0 :

        return
    
    print(nbTours,":")

    imagePath = IMAGEDEBUTPATH + "1" + IMAGEFINPATH
    listeDeReseauxDeNeurones = []
    listeDeReseauxDeNeurones.append(init_CNN(imagePath, BASEDEDONNEEPATH))

    indiceMin = 0
    cost_moyen_min = calcul_cost_moyen(listeDeReseauxDeNeurones[indiceMin].coefficients())

    for _ in range(1, 1001) :

        structureNeuronaleTemporaire = init_CNN(imagePath, BASEDEDONNEEPATH)
        structureNeuronaleTemporaire.changer_coefs_randomly()
        listeDeReseauxDeNeurones.append(structureNeuronaleTemporaire)

        cost_moyen_a_tester = calcul_cost_moyen(structureNeuronaleTemporaire.coefficients())

        if cost_moyen_a_tester <= cost_moyen_min :

            indiceMin = len(listeDeReseauxDeNeurones) - 1
            cost_moyen_min = cost_moyen_a_tester
            print("Trouvé !!!")
        
        if cost_moyen_a_tester <= 1.5 :
            
            indiceReseauAMultiplier = len(listeDeReseauxDeNeurones) - 1
            print("Trouvé !")
            print(cost_moyen_a_tester)

            for _ in range(1, 101) : 

                structureNeuronaleTemporaire = init_CNN(imagePath, None, listeDeReseauxDeNeurones[indiceReseauAMultiplier].coefficients())
                structureNeuronaleTemporaire.changer_coefs(descente_de_gradient(2, structureNeuronaleTemporaire.coefficients()))
                listeDeReseauxDeNeurones.append(structureNeuronaleTemporaire)

                cost_moyen_a_tester = calcul_cost_moyen(structureNeuronaleTemporaire.coefficients())

                if cost_moyen_a_tester <= cost_moyen_min :

                    indiceMin = len(listeDeReseauxDeNeurones) - 1
                    cost_moyen_min = cost_moyen_a_tester
                    print("Trouvé !!!")

    sauvegarde_coefficients(listeDeReseauxDeNeurones[indiceMin].coefficients())

    print(calcul_cost_moyen(),"\n")
    training(nbTours - 1)

training(100)
print(calcul_cost_moyen())