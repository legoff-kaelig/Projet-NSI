import sqlite3
from neurones import *
from CNN_python_init import *

os.chdir("en_cours/CNN")

con = sqlite3.connect("champys_correspondance_base_de_donee.sqli")
cur = con.cursor()

request = """
CREATE TABLE IF NOT EXISTS CHAMPY (
id INTEGER PRIMARY KEY,
nom VARCHAR
);
"""

cur.execute(request)

request = """
INSERT INTO CHAMPY
(nom)
VALUES ("Cèpe")
"""

cur.execute(request)

request = """
INSERT INTO CHAMPY
(nom)
VALUES ("Morille")
"""

cur.execute(request)

con.commit()
con.close()