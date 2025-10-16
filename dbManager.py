import sqlite3
from sqlite3 import Error

class baseDatos:
    def __init__(self, ruta = "./", bd = "miBD.sqlite3"):
        self.bd = ruta + '/' + bd
        self.conexionSQL()
        
    def conexionSQL(self): #Se crea objeto para inicializar la conexion
        try:
            self.con = sqlite3.connect(self.bd)
            self.cursor = self.con.cursor()
        except Error:
            print(Error)
            
    def crearDB(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reconocimientos(
                            persona TEXT,
                            tiempo TIMESTAMP);""")
        
    def agregarRegistro(self, nombre, tiempo):
        self.cursor.execute("""INSERT INTO reconocimientos (persona, tiempo) 
                            VALUES(?,?)""", (nombre, tiempo))
        self.con.commit()     
    
    