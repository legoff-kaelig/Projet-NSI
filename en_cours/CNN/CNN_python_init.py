from neurones import *
from random import *
from PIL.Image import *
import sqlite3
import os

def init_CNN(imagePath, baseDeDoneePath = None, coefficients = None) :

    assert baseDeDoneePath != coefficients

    ############################################################
     ############### Initialisation des variables ###############
      ############################################################

    baseDeDonneeEnArgument = coefficients == None

    if baseDeDonneeEnArgument :

        con = sqlite3.connect(baseDeDoneePath)
        cur=con.cursor()
        coefficients = [[], [], []]

    structureNeuronale = [[], [], [], []]
 
    image = open(imagePath)
    largeurImage, hauteurImage = image.size
    imagePxParPxMaisEnGris = []

      ############################################################
     ############################################################
    ############################################################


    #############################################################################################################################################################################
     ############## Remplissage du réseau neuronal par les neurones (avec les coefficients de la base de donnée "CNN_base_de_donnee.sqli" ou les pixels de l'image ###############
      #############################################################################################################################################################################


    ################ Mise en niveau de gris entre 0 et 1 et ajout au réseau de neurone de l'image ################

    for ligne in range(largeurImage) :

        for colonne in range(hauteurImage) :

            r,g,b,a = image.getpixel((ligne, colonne))
            niveauDeGris = (r + g + b) // 3
            imagePxParPxMaisEnGris.append(niveauDeGris)

    for px in imagePxParPxMaisEnGris :

        structureNeuronale[0].append(sigmoid(px))

    ##############################################################################################################

    ################ Ajout de la première couche de neurones ################

    if baseDeDonneeEnArgument :

        for neurone in range(13) :

            coefficients[0].append([])
            
            request = f"""
            SELECT *
            FROM COUCHE0NEURONE{neurone}
            """
            cur.execute(request)

            res = cur.fetchall()

            for indiceCoef in range(len(structureNeuronale[0])) :

                coefficients[0][neurone].append(res[indiceCoef][1])

    neuroneCouche1Numero1 = Neurone(coefficients[0][0])
    neuroneCouche1Numero2 = Neurone(coefficients[0][1])
    neuroneCouche1Numero3 = Neurone(coefficients[0][2])
    neuroneCouche1Numero4 = Neurone(coefficients[0][3])
    neuroneCouche1Numero5 = Neurone(coefficients[0][4])
    neuroneCouche1Numero6 = Neurone(coefficients[0][5])
    neuroneCouche1Numero7 = Neurone(coefficients[0][6])
    neuroneCouche1Numero8 = Neurone(coefficients[0][7])
    neuroneCouche1Numero9 = Neurone(coefficients[0][8])
    neuroneCouche1Numero10 = Neurone(coefficients[0][9])
    neuroneCouche1Numero11 = Neurone(coefficients[0][10])
    neuroneCouche1Numero12 = Neurone(coefficients[0][11])
    neuroneCouche1Numero13 = Neurone(coefficients[0][12])

    structureNeuronale[1] = [neuroneCouche1Numero1, 
                            neuroneCouche1Numero2, 
                            neuroneCouche1Numero3, 
                            neuroneCouche1Numero4, 
                            neuroneCouche1Numero5, 
                            neuroneCouche1Numero6, 
                            neuroneCouche1Numero7, 
                            neuroneCouche1Numero8, 
                            neuroneCouche1Numero9, 
                            neuroneCouche1Numero10, 
                            neuroneCouche1Numero11, 
                            neuroneCouche1Numero12, 
                            neuroneCouche1Numero13]

    #########################################################################

    ################ Ajout de la deuxième couche de neurones ################

    if baseDeDonneeEnArgument :

        for neurone in range(13) :

            coefficients[1].append([])
            
            request = f"""
            SELECT *
            FROM COUCHE1NEURONE{neurone}
            """

            cur.execute(request)

            res = cur.fetchall()

            for indiceCoef in range(len(structureNeuronale[1])) :

                coefficients[1][neurone].append(res[indiceCoef][1])

    neuroneCouche2Numero1 = Neurone(coefficients[1][0])
    neuroneCouche2Numero2 = Neurone(coefficients[1][1])
    neuroneCouche2Numero3 = Neurone(coefficients[1][2])
    neuroneCouche2Numero4 = Neurone(coefficients[1][3])
    neuroneCouche2Numero5 = Neurone(coefficients[1][4])
    neuroneCouche2Numero6 = Neurone(coefficients[1][5])
    neuroneCouche2Numero7 = Neurone(coefficients[1][6])
    neuroneCouche2Numero8 = Neurone(coefficients[1][7])
    neuroneCouche2Numero9 = Neurone(coefficients[1][8])
    neuroneCouche2Numero10 = Neurone(coefficients[1][9])
    neuroneCouche2Numero11 = Neurone(coefficients[1][10])
    neuroneCouche2Numero12 = Neurone(coefficients[1][11])
    neuroneCouche2Numero13 = Neurone(coefficients[1][12])

    structureNeuronale[2] = [neuroneCouche2Numero1, 
                            neuroneCouche2Numero2, 
                            neuroneCouche2Numero3, 
                            neuroneCouche2Numero4, 
                            neuroneCouche2Numero5, 
                            neuroneCouche2Numero6, 
                            neuroneCouche2Numero7, 
                            neuroneCouche2Numero8, 
                            neuroneCouche2Numero9, 
                            neuroneCouche2Numero10, 
                            neuroneCouche2Numero11, 
                            neuroneCouche2Numero12, 
                            neuroneCouche2Numero13]

    #########################################################################

    ################ Ajout de la dernière couche de neurone ################

    if baseDeDonneeEnArgument :

        for neurone in range(10) :

            coefficients[2].append([])
            
            request = f"""
            SELECT *
            FROM COUCHE2NEURONE{neurone}
            """

            cur.execute(request)

            res = cur.fetchall()

            for indiceCoef in range(len(structureNeuronale[2])) :

                coefficients[2][neurone].append(res[indiceCoef][1])

    neuroneCouche3Numero1 = Neurone(coefficients[2][0])
    neuroneCouche3Numero2 = Neurone(coefficients[2][1])
    neuroneCouche3Numero3 = Neurone(coefficients[2][2])
    neuroneCouche3Numero4 = Neurone(coefficients[2][3])
    neuroneCouche3Numero5 = Neurone(coefficients[2][4])
    neuroneCouche3Numero6 = Neurone(coefficients[2][5])
    neuroneCouche3Numero7 = Neurone(coefficients[2][6])
    neuroneCouche3Numero8 = Neurone(coefficients[2][7])
    neuroneCouche3Numero9 = Neurone(coefficients[2][8])
    neuroneCouche3Numero10 = Neurone(coefficients[2][9])

    structureNeuronale[3] = [neuroneCouche3Numero1, 
                            neuroneCouche3Numero2, 
                            neuroneCouche3Numero3, 
                            neuroneCouche3Numero4, 
                            neuroneCouche3Numero5, 
                            neuroneCouche3Numero6, 
                            neuroneCouche3Numero7, 
                            neuroneCouche3Numero8, 
                            neuroneCouche3Numero9, 
                            neuroneCouche3Numero10]

    #########################################################################

    reseauDeNeurones = ReseauDeNeurones(structureNeuronale)

      #############################################################################################################################################################################
     #############################################################################################################################################################################
    #############################################################################################################################################################################

    return(reseauDeNeurones)