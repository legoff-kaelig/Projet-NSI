from random import random
import math

def sigmoid(x):

    sig = 1 / (1 + math.exp(-x))
    return sig

def func_de_base_somme(termes) :

        resultat = 0

        for nombre in termes :

            resultat += nombre

        return resultat

class Neurone :

    def __init__(self, coefficients, func = func_de_base_somme, biais = 0) :

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