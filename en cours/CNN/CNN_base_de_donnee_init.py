import sqlite3
from random import *
from PIL.Image import *

structureNeuronale = [[[],[],[],[],[],[],[],[],[],[],[],[],[]],
                       [[],[],[],[],[],[],[],[],[],[],[],[],[]],
                       [[],[],[],[],[],[],[],[],[],[]]]
nbCouches = len(structureNeuronale)

image = open("C:/Users/Riwan/Documents/GitHub/Projet-NSI/en cours/CNN/nombres écrits à la main pour entrainer un modèle basique de reconnaissance d'image/7.png")
largeurImage, hauteurImage = image.size
imagePxParPxMaisEnGris = []

con = sqlite3.connect("CNN_base_de_donee.sqli")
cur=con.cursor()

request = """
CREATE TABLE IF NOT EXISTS CNN (
couches INTEGER PRIMARY KEY,
types VARCHAR
);
"""

cur.execute(request)

request = """
INSERT INTO CNN
(types)
VALUES ("Inputs")
"""

cur.execute(request)

for couche in range(nbCouches) :

    request = """
    INSERT INTO CNN
    (types)
    VALUES ("Neurones")
    """

    cur.execute(request)

    request = f"""
    CREATE TABLE IF NOT EXISTS COUCHES{couche} (
    neurones INTEGER PRIMARY KEY,
    biais
    );
    """

    cur.execute(request)

    for neurone in range(len(structureNeuronale[couche])) :

        biaisRandom = uniform(-15, 15)

        request = f"""
        INSERT INTO COUCHES{couche}
        (neurones, biais)
        VALUES ({neurone}, {biaisRandom})
        """

        cur.execute(request)
        
        request = f"""
        CREATE TABLE IF NOT EXISTS COUCHE{couche}NEURONE{neurone} (
        ID INTEGER PRIMARY KEY,
        coefficient
        );
        """

        cur.execute(request)

        if couche == 0 :

            nbCoefficients = largeurImage * hauteurImage
        
        else :
            
            nbCoefficients = len(structureNeuronale[couche - 1])

        for coefficient in range(nbCoefficients) :

            coefRandom = uniform(-5, 5)

            request = f"""
            INSERT INTO COUCHE{couche}NEURONE{neurone}
            (coefficient)
            VALUES ({coefRandom})
            """

            cur.execute(request)


con.commit()
con.close()

# ################ Mise en niveau de gris entre 0 et 1 de l'image ################

# for ligne in range(largeurImage) :

#     for colonne in range(hauteurImage) :

#         r,g,b,a = image.getpixel((ligne, colonne))
#         niveauDeGris = (r + g + b) // 3
#         imagePxParPxMaisEnGris.append(niveauDeGris)

# for px in imagePxParPxMaisEnGris :

#     structureNeuronale[0].append(sigmoid(px))

# ################################################################################