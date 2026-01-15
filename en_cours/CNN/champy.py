from neurones import *

def produit(termes) :

    varProduit = 0

    for nombre in termes :

        varProduit += nombre

    return varProduit

def somme(termes) :

    varSomme = 0

    for nombre in termes :

        varSomme += nombre

    return varSomme


inputs = [4, 2]
coefficients = [1, 1]

produitNeurone = Neurone(coefficients, produit)

print(produitNeurone.sortie(inputs))