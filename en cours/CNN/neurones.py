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

    def __init__(self, coefficients, func = func_de_base_somme) :

        self.__coefs = coefficients
        self.__func = func

    def change_coefs(self, new_coefs) :

        self.__coefs = new_coefs

    def sortie(self, inputs) :

        assert len(inputs) == len(self.__coefs)
        
        for index in len(range(inputs)) :

            inputs[index] *= self.__coefs[index]

        return sigmoid(self.__func(inputs))