from random import random
import math

def sigmoid(x):
    """
    Entrée : <x> un réel

    Sortie : un flottant compris entre 0 et 1
    """

    sig = 1 / (1 + math.exp(-x))
    return sig



def func_de_base_somme(termes) :
    """
    Entrée : <termes> une liste de réels

    Sortie : La somme de tous ces termes
    """
    resultat = 0

    for nombre in termes :

        resultat += nombre

    return resultat



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

        return self.__coefs
    


    def biais(self) :

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

            new_coefs.append(random())

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

    def changer_inputs(self, new_inputs) :
        """
        Entrée : <new_inputs>, la liste des nouveaux inputs à mettre

        Action : Changement des valeurs de l'attribut <__inputs> pour ceux de <new_inputs>
        """

        self.__inputs = new_inputs
    


    def multiplier_coefs(self, new_coefs) :
        """
        Entrée : <new_coefs>, les coefficients à appliquer sur les anciens coefficients

        Action : Multiplication de tous les coefficients des neurones du réseau par leur correspondant dans <new_coefs> 
        """

        assert len(new_coefs) == len(self.__couches)

        for indiceCouche in range(len(self.__couches)) :

            for neurone in self.__couches[indiceCouche] :

                new_coefs_neurone = []

                for indiceCoef in range(len(neurone.coefs())) :

                    new_coefs_neurone.append(neurone.coefs()[indiceCoef] * new_coefs[indiceCouche][indiceCoef])

                neurone.changer_coefs(new_coefs_neurone)
    
    

    def sortie(self) :

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
