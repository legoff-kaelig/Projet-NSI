class Neurone :

    def __init__(self, coefficients, func) :

        self.__coefs = coefficients
        self.__func = func

    def change_coefs(self, new_coefs) :

        self.__coefs = new_coefs

    def sortie(self, inputs) :

        assert len(inputs) == len(self.__coefs)
        
        for index in range(len(inputs)) :

            inputs[index] *= self.__coefs[index]

        return self.__func(inputs)