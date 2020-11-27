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
            sql = db.text("""SELECT t1.id,
                                    t1.nombre_algoritmo,
                                    t1.parametros,
                                    t1.inicio,
                                    t1.fin,
                                    t1.estado,
                                    MIN(t2.fitness_mejor) as fitness
                            FROM datos_ejecucion t1
                            LEFT JOIN datos_iteracion t2 ON t1.id=t2.id_ejecucion

                            
                            GROUP BY 
                                    t1.id,
                                    t1.nombre_algoritmo,
                                    t1.parametros,
                                    t1.inicio,
                                    t1.fin,
                                    t1.estado
                             """)

            # **{"nombre_algoritmo":algoritmo}
            result = connection.execute(sql).fetchall()
            return result

        except db.exc.SQLAlchemyError as e:

            return False
        
    def getIteracionesByAlgInst(self,algorithm,instance):

        try: 
            connection = self.engine.connect()
            sql = db.text("""SELECT t1.id,
                                    t1.nombre_algoritmo,
                                    t2.numero_iteracion,
                                    t2.fitness_mejor as fitness,
                                    t2.parametros_iteracion
                                    
                            FROM datos_ejecucion t1
                            LEFT JOIN datos_iteracion t2 ON t1.id=t2.id_ejecucion
                            
                            WHERE t1.nombre_algoritmo = :algorithm
                            and t1.parametros like :instance
                            
                            ORDER BY t1.id,t2.numero_iteracion ASC
                            """)

            # **{"nombre_algoritmo":algoritmo}
            result = connection.execute(sql,**{"algorithm":algorithm,"instance": f"%{instance}%"}).fetchall()
            return result

        except db.exc.SQLAlchemyError as e:
            print(e)

            return False
        
        