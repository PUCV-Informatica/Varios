# Utils
import sys
import os
from envs import env
from datetime import datetime
from dotenv import load_dotenv

#Load environments
from dotenv import load_dotenv
load_dotenv()

# SQL
import sqlalchemy as db
import psycopg2
import json
import pickle
import zlib

class Database:

    def __init__(self):

        # Definicion Environments Vars
        db_motor = env('DB_MOTOR')
        db_user = env('DB_USER')
        db_pass = env('DB_PASS')
        db_server = env('DB_SERVER')
        db_port = env('DB_PORT')
        db_base   = env('DB_BASE')

        # Conexión a la DB de resultados
        self.engine = db.create_engine(f'{db_motor}://{db_user}:{db_pass}@{db_server}:{db_port}/{db_base}')
        self.metadata = db.MetaData()

    def getEjecuciones(self):

        try: 
            connection = self.engine.connect()
            sql = db.text("""SELECT * FROM datos_ejecucion""")

            # **{"nombre_algoritmo":algoritmo}
            result = connection.execute(sql).fetchall()

            return result

        except db.exc.SQLAlchemyError as e:

            return False
        
    def getEjecucionesResultados(self):

        try: 
            connection = self.engine.connect()
            sql = db.text("""SELECT * FROM resultado_ejecucion """)

            # **{"nombre_algoritmo":algoritmo}
            result = connection.execute(sql).fetchall()

            return result

        except db.exc.SQLAlchemyError as e:

            return False