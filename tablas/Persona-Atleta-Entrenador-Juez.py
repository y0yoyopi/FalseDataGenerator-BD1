from faker import Faker
import random
import os
import pandas as pd

fake = Faker()

# Directorios de salida
output_dirs = {
    "personas": "csv/Personas",
    "atletas": "csv/Atletas",
    "jueces": "csv/Jueces",
    "entrenadores": "csv/Entrenadores",
}

# Crear directorios
for key, path in output_dirs.items():
    os.makedirs(path, exist_ok=True)

# Función para generar datos de personas
def generar_datos_persona(num_personas):
    personas = []
    for i in range(1, num_personas + 1):
        persona = {
            "ID_persona": i,
            "nombre": fake.name(),
            "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d'),
            "edad": None,  # Se calcula en la base de datos con un trigger
            "genero": fake.random_element(elements=["Masculino", "Femenino"]),
            "nacionalidad": fake.random_element(elements=["Peruano", "Chileno", "Argentino", "Mexicano", "Español"])
        }
        personas.append(persona)
    return personas

# Función para generar datos de atletas
def generar_datos_atleta(num_atletas, persona_ids, max_equipo_id, max_arte_marcial_id, max_categoria_id):
    atletas = []
    for i in range(num_atletas):
        atleta = {
            "ID_persona": random.choice(persona_ids),
            "ID_equipo": random.randint(1, max_equipo_id),
            "ID_arte_marcial": random.randint(1, max_arte_marcial_id),
            "ID_categoria": random.randint(1, max_categoria_id),
        }
        atletas.append(atleta)
    return atletas

# Función para generar datos de jueces
def generar_datos_juez(num_jueces, persona_ids):
    jueces = []
    for i in range(num_jueces):
        juez = {
            "ID_persona": random.choice(persona_ids),
            "tipo": fake.random_element(elements=["Principal", "Auxiliar", "Árbitro"]),
        }
        jueces.append(juez)
    return jueces

# Función para generar datos de entrenadores
def generar_datos_entrenador(num_entrenadores, persona_ids, max_equipo_id):
    entrenadores = []
    for i in range(num_entrenadores):
        entrenador = {
            "ID_persona": random.choice(persona_ids),
            "ID_equipo": random.randint(1, max_equipo_id),
        }
        entrenadores.append(entrenador)
    return entrenadores

# Función para guardar datos en un CSV
def guardar_csv(datos, directorio, nombre_archivo):
    df = pd.DataFrame(datos)
    filepath = os.path.join(directorio, nombre_archivo)
    df.to_csv(filepath, index=False, sep=";")
    print(f"Archivo {nombre_archivo} generado en {directorio}.")

# Generar datos para las tablas
def generar_datos_completos():
    tamanos = [1000, 10000, 100000, 1000000]
    max_equipo_id, max_arte_marcial_id, max_categoria_id = 100, 10, 50

    for tamano in tamanos:
        # Generar personas (3x el tamaño base)
        num_personas = tamano * 3
        personas = generar_datos_persona(num_personas)
        guardar_csv(personas, output_dirs["personas"], f"personas_{num_personas}.csv")

        # IDs de personas divididas para cada rol
        persona_ids = list(range(1, num_personas + 1))
        atleta_ids = persona_ids[:tamano]
        juez_ids = persona_ids[tamano:tamano * 2]
        entrenador_ids = persona_ids[tamano * 2:]

        # Generar atletas
        atletas = generar_datos_atleta(tamano, atleta_ids, max_equipo_id, max_arte_marcial_id, max_categoria_id)
        guardar_csv(atletas, output_dirs["atletas"], f"atletas_{tamano}.csv")

        # Generar jueces
        jueces = generar_datos_juez(tamano, juez_ids)
        guardar_csv(jueces, output_dirs["jueces"], f"jueces_{tamano}.csv")

        # Generar entrenadores
        entrenadores = generar_datos_entrenador(tamano, entrenador_ids, max_equipo_id)
        guardar_csv(entrenadores, output_dirs["entrenadores"], f"entrenadores_{tamano}.csv")

# Ejecutar la generación de datos
if __name__ == "__main__":
    generar_datos_completos()
