from neurones import *
from CNN_python_init import *

os.chdir("en_cours/CNN")

IMAGEPATH = os.path.join(os.getcwd(),"nombres écrits à la main pour entrainer un modèle basique de reconnaissance d'image/0.png")
BASEDEDONNEEPATH = "CNN_base_de_donee.sqli"

def sortie_max() :

    sortiesEnListe = init_CNN(IMAGEPATH, BASEDEDONNEEPATH).sortie()

    print(sortiesEnListe)

    indiceSortieMax = 0

    for i in range(len(sortiesEnListe)) :
        
        if sortiesEnListe[i] > sortiesEnListe[indiceSortieMax] :

            indiceSortieMax = i
        
    return indiceSortieMax

print(sortie_max())