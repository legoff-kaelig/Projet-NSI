import sqlite3
import os

os.chdir("en_cours/CNN")


con = sqlite3.connect("CNN_base_de_donee.sqli")
cur=con.cursor()

request = f"""
UPDATE COUCHE0NEURONE0
SET coefficient = 1
WHERE ID = 1
"""

cur.execute(request)

request = f"""
UPDATE COUCHE1NEURONE0
SET coefficient = 1
WHERE ID = 1
"""

cur.execute(request)

request = f"""
UPDATE COUCHE2NEURONE0
SET coefficient = 1
WHERE ID = 1
"""

cur.execute(request)

con.commit()
con.close()