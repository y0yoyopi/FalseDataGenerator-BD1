# utils.py

import pandas as pd
import os

# Crear directorio de salida para Atleta
output_dir = "Atleta"
os.makedirs(output_dir, exist_ok=True)

def guardar_csv(datos, nombre_archivo):
    """
    Guarda una lista de diccionarios como un archivo CSV.
    :param datos: Lista de diccionarios con los datos.
    :param nombre_archivo: Nombre del archivo CSV (sin la ruta).
    """
    filepath = os.path.join(output_dir, nombre_archivo)
    df = pd.DataFrame(datos)
    df.to_csv(filepath, index=False, sep=";")
    print(f"Archivo '{nombre_archivo}' generado con éxito en la carpeta '{output_dir}'.")

def extraer_subconjunto(datos, num_registros):
    """
    Extrae los primeros num_registros de una lista de datos.
    :param datos: Lista de diccionarios con los datos.
    :param num_registros: Número de registros a extraer.
    :return: Subconjunto de datos.
    """
    return datos[:num_registros]

def guardar_subconjuntos_csv(subconjunto, nombre_archivo):
    """
    Guarda un subconjunto de datos como un archivo CSV.
    :param subconjunto: Lista de diccionarios con los datos.
    :param nombre_archivo: Nombre del archivo CSV (sin la ruta).
    """
    filepath = os.path.join(output_dir, nombre_archivo)
    df = pd.DataFrame(subconjunto)
    df.to_csv(filepath, index=False, sep=";")
    print(f"Archivo '{nombre_archivo}' generado con {len(subconjunto)} registros en la carpeta '{output_dir}'.")
