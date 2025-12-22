from random import random
import math

def sigmoid(x):
    """
    Entrée : <x> un réel

    Sortie : un flottant strictement copris entre 0 et 1
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



    def sortie(self, inputs : list) :
        """
        Entrée : <inputs>, la liste des nombres à faire passer dans la fonction du neurone

        Sortie : La sortie de la fonction du neurones où les inputs ont été multipliés par les coefs et où le biais à été rajouté
        """

        assert len(inputs) <= len(self.__coefs)
        
        for index in range(len(inputs)) :

            inputs[index] *= self.__coefs[index]

        inputs.append(self.__biais)

        return sigmoid(self.__func(inputs))