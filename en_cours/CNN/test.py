from neurones import *
from CNN_python_init import *

os.chdir("en_cours/CNN")

IMAGEPATH = os.path.join(os.getcwd(),"champis images/1.jpg")
BASEDEDONNEEPATH = "CNN_base_de_donee.sqli"

def resultat_CNN(reseauDeNeurones : ReseauDeNeurones) :
    """
    Entrées :
        - <reseauDeNeurones> : Un réseau de neurones

    Sortie :
        - <resultatMax> : La sortie prépondérante dans la liste des sorties du réseau de neurone
    """
    results = reseauDeNeurones.sortie()

    resultatMax = 0

    for indexResult in range(len(results)) :

        if results[indexResult] > results[resultatMax] :

            resultatMax = indexResult

    return resultatMax

reseau = init_CNN(IMAGEPATH, BASEDEDONNEEPATH)


print(reseau.sortie())
print(resultat_CNN(reseau))