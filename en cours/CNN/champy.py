from neurones import *

def produit(termes) :
    a,b = termes
    return a * b

inputs = [1, 2]
coefficients = [1, 1]

produitNeurone = Neurone(coefficients, produit)

print(produitNeurone.sortie(inputs))