import os
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])


secret='ca45c6d3e7a6787b0b5275a942643f504924e6b13cd1a293'
algorithm='HS256'

db_path = f'{homeDir}\\db.db'