# import sqlite3

# con = sqlite3.connect("Test.sqli")
# cur=con.cursor()

# a = 5

# for i in range(a) :

#     request = f"""
#     CREATE TABLE IF NOT EXISTS TEST{i} (
#     column_1 INTEGER
#     );
#     """

#     cur.execute(request)

# request = """
# INSERT INTO TEST1 
# (column_1)
# VALUES (2)
# """

# cur.execute(request)
# cur.execute(request)

# for i in range(a) :

#     request = f"""
#     SELECT *
#     FROM TEST{i}
#     """

#     cur.execute(request)

#     res = cur.fetchall()
#     print(res)

# con.commit()
# con.close()

from random import *


print(uniform(-5, 5))