from neurones import *
from random import *
from PIL.Image import *

image = open("C:/Users/Riwan/Documents/GitHub/Projet-NSI/en cours/CNN/nombres écrits à la main pour entrainer un modèle basique de reconnaissance d'image/9.png")

largeurImage, hauteurImage = image.size
imagePxParPxMaisEnGris = []

for ligne in range(largeurImage) :

    for colonne in range(hauteurImage) :

        r,g,b,a = image.getpixel((ligne, colonne))
        niveauDeGris = (r + g + b) // 3
        imagePxParPxMaisEnGris.append(niveauDeGris)

coefficients = [[],[]]

for couche in range(len(coefficients)) :

    for numero in range(13) :

        coefficients[couche].append(random())  

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

