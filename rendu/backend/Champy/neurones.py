#### Librairie permettant de gérer un Réseau de Neurones et des Neurones ####
from random import *
from PIL.Image import *
import math

def sigmoid(x):
    """
    Entrée : <x> un réel

    Sortie : un flottant compris entre 0 et 1
    """
    if x >= 0:

        return 1 / (1 + math.exp(-x))
    
    else:
        
        return math.exp(x) / (1 + math.exp(x))
    


def sigmoid_derivee(x) :
    """
    Entrée : <x> un réel

    Sortie : Le nombre dérivé de sigmoid(x)
    """
    return math.exp(-x) / ((1 + math.exp(-x))**2)



def func_de_base_somme(termes) :
    """
    Entrée : <termes> une liste de réels

    Sortie : La somme de tous ces termes
    """
    resultat = 0

    for nombre in termes :

        resultat += nombre

    return resultat



def convolution(imagePath) :
    """
    Entrée :
        - <imagePath> : Le chemin d'accès vers une image

    Sortie :
        - <newInputs> : La liste des inputs basés sur l'image en nuance de gris
    """
    image = open(imagePath)
    largeurImage, hauteurImage = image.size
    imagePxParPxMaisEnGris = []
    newInputs = []

    for ligne in range(largeurImage) :

        for colonne in range(hauteurImage) :

            r,g,b,a = image.getpixel((ligne, colonne))
            niveauDeGris = (r + g + b) // 3
            imagePxParPxMaisEnGris.append(niveauDeGris)

    for px in imagePxParPxMaisEnGris :

        newInputs.append(sigmoid(px))

    return newInputs


class Neurone :

    def __init__(self, coefficients, func = func_de_base_somme, biais = 0) :
        """
        Entrée :

            <coefficients>, la liste des coefficients du neurone
            <func>, la fonction que va effectuer le neurone, de base une somme
            <biais>, le biais du neurone

        Action : Création des attributs éponymes aux entrées pour notre neurone
        """

        self.__coefs = coefficients
        self.__func = func
        self.__biais = biais



    def coefs(self) :
        """
        Sortie :
            - <coefsARetourner> : La liste des coefficients du neurone
        """
        coefsARetourner = []

        for coef in self.__coefs :
            
            coefsARetourner.append(coef)

        return coefsARetourner
    


    def biais(self) :
        """
        Sortie :
            - <biais> : Le biais du neurone
        """
        return self.__biais
    


    def changer_coefs(self, new_coefs) :
        """
        Entrée : <new_coefs>, la liste des nouveaux coefficients à ajouter

        Action : Modification de la liste attribut du neurones <__coefs>
        """
        
        self.__coefs = new_coefs



    def changer_coefs_randomly(self, nb_coefs) :
        """
        Entrée : <nb_coefs>, un entier naturel correspondant au nombre de coefs voulus

        Action : Change l'attribut du neurone <__coefs> en une liste de longueur <nb_coefs> de nombres aléatoires compris entre 0 et 1 
        """

        new_coefs = []

        for _ in range(nb_coefs) :

            new_coefs.append(uniform(-15, 15))

        self.changer_coefs(new_coefs)



    def sortie(self, inputsSortie : list) :
        """
        Entrée : <inputs>, la liste des nombres à faire passer dans la fonction du neurone

        Sortie : La sortie de la fonction du neurones où les inputs ont été multipliés par les coefs et où le biais à été rajouté
        """

        assert len(inputsSortie) == len(self.__coefs)

        inputsFunc = []
        
        for index in range(len(inputsSortie)) :

            inputsFunc.append(inputsSortie[index] * self.__coefs[index])

        inputsFunc.append(self.__biais)

        return sigmoid(self.__func(inputsFunc))
    


    def derivee_partielle(self, indiceCoefADeriver, inputsSortie : list) :
        """
        Entrée :
            - <indiceCoefADeriver> : L'indice du coef pour lequel on va dériver partiellement la fonction
            - <inputs> : La liste des nombres à faire passer dans la fonction dérivée du neurone

        Sortie : La sortie de la fonction dérivée du neurones en fonction du coef
        """
        assert len(inputsSortie) == len(self.__coefs)

        inputsFunc = []
        
        inputsFunc.append(inputsSortie[indiceCoefADeriver])

        inputsFunc.append(self.__biais)

        return sigmoid_derivee(self.__func(inputsFunc))



class ReseauDeNeurones :

    def __init__(self, matriceDuReseau) :
        """
        Entrée : <matriceDuReseau>, une matrice contenant au moins une première couches de nombres entre 0 et 1 et et une deuxième couche de neurones avec chacuns le même nombre de coefficients que de nombres ou de neurones dans la couche précédente, cette matrice est la base du reseau neuronal 

        Action : Création de deux attributs, <__inputs> la première couche du réseau contenant de simple nombres entre 0 et 1 et <__couches> une matrice contenant les couches de neurones suivantes
        """

        self.__inputs = matriceDuReseau[0]
        self.__couches = []

        for couche in range(1,len(matriceDuReseau)) :

            self.__couches.append(matriceDuReseau[couche])
        
        self.__sorties = self.sortie_init()



    def inputs(self) :
        """
        Sortie : <self.__inputs>, les inputs du réseau de neurone
        """

        return self.__inputs



    def couches(self) :
        """
        Sortie : <self.__couche>, les couches de notre réseau de neurones
        """

        return self.__couches
    
    

    def coefficients(self) :
        """
        Sortie :
            - La liste de tous les coeffs du réseau de neurones
        """
        coefsTotaux = []

        for couche in self.__couches :

            coefsLocaux = []

            for neurone in couche :

                coefsLocaux.append(neurone.coefs())

            coefsTotaux.append(coefsLocaux)

        return coefsTotaux



    def changer_inputs(self, newInputs) :
        """
        Entrée : <newInputs>, la liste des nouveaux inputs à mettre

        Action : Changement des valeurs de l'attribut <__inputs> pour ceux de <newInputs>
        """

        self.__inputs = newInputs
        self.__sorties = self.sortie_init()

    

    def changer_inputs_image(self, imagePath) :
        """
        Entrée : <imagePath>, le chemin vers l'image pour lequel on en extraira des inputs

        Action : Changement des valeurs de l'attribut <__inputs> pour ceux de convolution(imagePath)
        """
        self.changer_inputs(convolution(imagePath))



    def multiplier_coefs(self, new_coefs) :
        """
        Entrée : <new_coefs>, les coefficients à appliquer sur les anciens coefficients

        Action : Multiplication de tous les coefficients des neurones du réseau par leur correspondant dans <new_coefs> 
        """

        assert len(new_coefs) == len(self.__couches)

        for indiceCouche in range(len(self.__couches)) :

            for neurone in self.__couches[indiceCouche] :

                new_coefs_neurone = []
                old_coefs_neurone = neurone.coefs()

                for indiceCoef in range(len(old_coefs_neurone)) :

                    new_coefs_neurone.append(old_coefs_neurone[indiceCoef] * new_coefs[indiceCouche][indiceCoef])

                neurone.changer_coefs(new_coefs_neurone)

        self.__sorties = self.sortie_init()


    
    def changer_coefs(self, newCoefs) :
        """
        Entrée : <newCoefs>, la liste des coefficients à mettre

        Action : Changement de tous les coefficients des neurones du réseau par leur correspondant dans <newCoefs> 
        """

        assert len(newCoefs) == len(self.__couches)

        for indiceCouche in range(len(self.__couches)) :

            for indiceNeurone in range(len(self.__couches[indiceCouche])) :

                new_coefs_neurone = []
                old_coefs_neurone = self.__couches[indiceCouche][indiceNeurone].coefs()

                for indiceCoef in range(len(old_coefs_neurone)) :

                    new_coefs_neurone.append(newCoefs[indiceCouche][indiceNeurone][indiceCoef])

                self.__couches[indiceCouche][indiceNeurone].changer_coefs(new_coefs_neurone)

        self.__sorties = self.sortie_init()



    def multiplier_coefs_randomly(self, ecart) :
        """
        Action : Multiplication de tous les coefficients des neurones du réseau par un nombre àléatoire entre -15 et 15
        """

        for indiceCouche in range(len(self.__couches)) :

            for neurone in self.__couches[indiceCouche] :

                new_coefs_neurone = []
                old_coefs_neurone = neurone.coefs()

                for indiceCoef in range(len(old_coefs_neurone)) :

                    new_coefs_neurone.append(old_coefs_neurone[indiceCoef] * uniform(-ecart, ecart))

                neurone.changer_coefs(new_coefs_neurone)

        self.__sorties = self.sortie_init()
    
    

    def changer_coefs_randomly(self) :
        """
        Action : Changement de tous les coefficients des neurones du réseau par un nombre àléatoire entre -15 et 15
        """

        for indiceCouche in range(len(self.__couches)) :

            for neurone in self.__couches[indiceCouche] :

                new_coefs_neurone = []
                old_coefs_neurone = neurone.coefs()

                for indiceCoef in range(len(old_coefs_neurone)) :

                    new_coefs_neurone.append(uniform(-15, 15))

                neurone.changer_coefs(new_coefs_neurone)

        self.__sorties = self.sortie_init()
    


    def sortie_init(self) :

        """
        Entrée : <inputs>, la liste des liste de nombres à faire passer dans les fonctions des neurones

        Sortie : La sortie des neurones de la dernière couche
        """

        listeDesInputs = []
        listeDesInputs.append(self.__inputs)
        

        for couche in self.__couches :
            
            listeDesResultats = []

            for neurone in couche :

                listeDesResultats.append(neurone.sortie(listeDesInputs[0]))

            listeDesInputs.pop()
            listeDesInputs.append(listeDesResultats)
            
        return listeDesResultats
    


    def derivee_partielle(self, indiceCoefADeriver, indiceNeuroneCoefADeriver, indiceCoucheCoefADeriver) :

        listeDesInputs = []
        listeDesInputs.append(self.__inputs)

        for couche in self.__couches :
            
            listeDesResultats = []

            if self.__couches[indiceCoucheCoefADeriver] == couche :

                for neurone in couche :

                    if couche[indiceNeuroneCoefADeriver] == neurone :

                        listeDesResultats.append(neurone.derivee_partielle(indiceCoefADeriver, listeDesInputs[0]))

                    listeDesResultats.append(0)

            else :

                for _ in couche :

                    listeDesResultats.append(0)

            listeDesInputs.pop()
            listeDesInputs.append(listeDesResultats)

        return listeDesResultats
    


    def sortie(self) :
        """
        Sortie :
            - La liste des sorties du réseau de neurone
        """
        return self.__sorties