# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:31:05 2025

@author: dtrej
"""

from deepface import DeepFace
import cv2
import pyttsx3
from dbManager import baseDatos as bd
import datetime

def reconocimiento(frame):
    try:
        #Detecta a la persona que salga y este en la base de datos
        recognition = DeepFace.find(frame, db_path="db", model_name="VGG-Face", silent=True)
        
        if len(recognition) > 0:  # Verificar si se detectaron rostros
            recognition_df = recognition[0]  # Tomar el primer DataFrame de la lista
            if not recognition_df.empty:  # Verificar si el DataFrame tiene datos
                recognition2 = recognition_df["identity"].iloc[0]  # Obtener la primera identidad
                nombre = recognition2.split("\\")[1].split("/")[0]
                return nombre
        
        return "Rostro no detectado"
    
    except (ValueError, KeyError, IndexError):
        return "Rostro no detectado"


def saludar(mensaje):
    engine.say("hola" + mensaje)
    engine.runAndWait()

def guardarDB(base, mensaje):
    base.agregarRegistro(mensaje, datetime.datetime.now())

base = bd()
base.crearDB()
vid = cv2.VideoCapture(0) #Seleccion de camara de la computadora

engine = pyttsx3.init() #Motor para reproducir audio
engine.setProperty('rate', 125) #Velocidad a la que va a hablar la computadora

mensajeAnterior=''
cv2.namedWindow("Proyecto", cv2.WINDOW_NORMAL) #Nombre de la ventana de la camara

while True:
    ret, frame = vid.read() #Se comienza a leer la camara
    if not ret: #si no detecta una camara acaba el programa
        break
    
    mensaje = reconocimiento(frame) #Se manda a llamar la funcion reconocimiento para detectar a la persona
                                    #y leer el nombre de la persona que se detecto o si no se detecto a nadie
    
    if mensaje != mensajeAnterior and mensaje != "Rostro no detectado":  #Si lo que detecta en la camara es diferente a lo que se detecto anteriormente
        guardarDB(base, mensaje)    
        saludar(mensaje)            #se reproduce audio si no no se reproduce nada
    
    cv2.putText(frame, mensaje, (0,115), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2) #Funcion para colocar texto en la camara
    cv2.imshow("Proyecto", frame) #Muestra la camara
    
    if cv2.waitKey(1) == ord('q'): #Orden para detener el programa
        break
    
    mensajeAnterior = mensaje #Actualizacion del mensaje

vid.release()
cv2.destroyAllWindows()