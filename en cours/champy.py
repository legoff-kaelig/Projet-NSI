class Neurone :

    def __init__(self, coefficients, func) :

        self.__coefs = coefficients
        self.__func = func

    def change_coefs(self, new_coefs) :

        self.__coefs = new_coefs

    def sortie(self, inputs) :

        assert len(inputs) == len(self.__coefs)
        
        for index in len(range(inputs)) :

            inputs[index] *= self.__coefs[index]

        return self.__func(inputs)

def produit(termes) :
    a,b = termes
    return a * b

inputs = [1, 2]
coefficients = [1, 1]

produitNeurone = Neurone(coefficients, produit)

print(produitNeurone.sortie(inputs))