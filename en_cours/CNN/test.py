# import sqlite3

# con = sqlite3.connect("CNN_base_de_donee.sqli")
# cur=con.cursor()

# request = f"""
# SELECT *
# FROM COUCHE1NEURONE2
# """

# cur.execute(request)

# res = cur.fetchall()
# print(res)

# con.commit()
# con.close()

# # from random import *


# # print(uniform(-5, 5))

import os

print(os.getcwd()) 
os.chdir("en_cours/CNN")
print(os.getcwd()) 