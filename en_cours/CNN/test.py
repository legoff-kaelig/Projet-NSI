from neurones import *
from CNN_python_init import *

os.chdir("en_cours/CNN")

IMAGEPATH = os.path.join(os.getcwd(),"nombres écrits à la main pour entrainer un modèle basique de reconnaissance d'image/7.png")
BASEDEDONNEEPATH = "CNN_base_de_donee.sqli"

def resultat_CNN(reseauDeNeurones : ReseauDeNeurones, resultatVoulu) :
    """
    Entrées :
        - <reseauDeNeurones> : Un réseau de neurones
    """
    results = reseauDeNeurones.sortie()

    resultatMax = 0

    for indexResult in range(len(results)) :

        if results[indexResult] > results[resultatMax] :

            resultatMax = indexResult

    return resultatMax

reseau = init_CNN(IMAGEPATH, BASEDEDONNEEPATH)
print(reseau.inputs())
print(reseau.sortie_init())