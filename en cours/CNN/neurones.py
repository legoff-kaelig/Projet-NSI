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

            :coefficients: La liste des coefficients du neurone
            :func: La fonction que va effectuer le neurone, de base une somme
            :biais: Le biais du neurone

        Action : Création des attributs éponymes aux entrées pour notre neurone
        """

        self.__coefs = coefficients
        self.__func = func
        self.__biais = biais

    def changer_coefs(self, new_coefs) :

        self.__coefs = new_coefs

    def cahnger_coefs_randomly(self) :
         
        self.__coefs = random()

    def sortie(self, inputs : list) :

        assert len(inputs) <= len(self.__coefs)
        
        for index in range(len(inputs)) :

            inputs[index] *= self.__coefs[index]

        inputs.append(self.__biais)

        return sigmoid(self.__func(inputs))