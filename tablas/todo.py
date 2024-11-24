import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

# Directorios de salida
output_dirs = {
    "personas": "csv/Personas",
    "jueces": "csv/Jueces",
    "atletas": "csv/Atletas",
    "entrenadores": "csv/Entrenadores",
    "equipos": "csv/Equipos",
    "competencias": "csv/Competencias",
    "combates": "csv/Combates",
}

# Crear directorios si no existen
for key, path in output_dirs.items():
    os.makedirs(path, exist_ok=True)

# Mantener un conjunto global de IDs únicos
used_ids = set()

# Generar IDs únicos
def generar_id_unico():
    while True:
        nuevo_id = random.randint(1, 10**9)
        if nuevo_id not in used_ids:
            used_ids.add(nuevo_id)
            return nuevo_id

# Generar personas
def generar_personas(num_personas):
    personas = []
    for _ in range(num_personas):
        persona = {
            "id_persona": generar_id_unico(),
            "nombre": fake.name(),
            "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=70),
            "edad": None,  # Se puede calcular con un trigger
            "genero": random.choice(["Masculino", "Femenino"]),
            "nacionalidad": random.choice(["Peruano", "Colombiano", "Chileno", "Argentino", "Mexicano"]),
        }
        personas.append(persona)
    return personas

# Generar jueces
def generar_jueces(num_jueces, personas):
    jueces = []
    for i in range(num_jueces):
        juez = {
            "id_persona": personas[i]["id_persona"],  # Usamos los IDs generados para persona
            "tipo": random.choice(["Árbitro", "Supervisor", "Juez Técnico"])
        }
        jueces.append(juez)
    return jueces

# Generar atletas
def generar_atletas(num_atletas, personas):
    atletas = []
    for i in range(num_atletas):
        atleta = {
            "id_persona": personas[i]["id_persona"],  # Usamos los IDs generados para persona
            "id_equipo": random.randint(1, 100),  # Ajustar según el número de equipos
            "id_arte_marcial": random.randint(1, 5),
            "id_categoria": random.randint(1, 10)  # Ajustar según categorías existentes
        }
        atletas.append(atleta)
    return atletas

# Generar entrenadores
def generar_entrenadores(num_entrenadores, personas):
    entrenadores = []
    for i in range(num_entrenadores):
        entrenador = {
            "id_persona": personas[i]["id_persona"],  # Usamos los IDs generados para persona
            "id_equipo": random.randint(1, 100)  # Ajustar según el número de equipos
        }
        entrenadores.append(entrenador)
    return entrenadores

# Generar equipos
def generar_equipos(num_equipos):
    equipos = []
    for _ in range(num_equipos):
        equipo = {
            "id_equipo": generar_id_unico(),
            "nombre": f"Equipo {fake.city()}",
            "id_arte_marcial": random.randint(1, 5)  # 5 artes marciales disponibles
        }
        equipos.append(equipo)
    return equipos

# Generar competencias
def generar_competencias(num_competencias):
    competencias = []
    for _ in range(num_competencias):
        competencia = {
            "id_competencia": generar_id_unico(),
            "nombre": fake.word().capitalize() + " Tournament",
            "fecha_inicio": fake.date_between(start_date="-1y", end_date="today"),
            "fecha_fin": fake.date_between(start_date="today", end_date="+1y"),
            "lugar": fake.city(),
        }
        competencias.append(competencia)
    return competencias

# Generar combates
def generar_combates(num_combates, atletas, jueces, competencias):
    combates = []
    for _ in range(num_combates):
        atleta_1 = random.choice(atletas)
        atleta_2 = random.choice([a for a in atletas if a["id_equipo"] != atleta_1["id_equipo"]])  # Asegurar diferentes equipos
        juez = random.choice(jueces)
        competencia = random.choice(competencias)
        
        combate = {
            "id_combate": generar_id_unico(),
            "id_juez": juez["id_persona"],
            "id_atleta_1": atleta_1["id_persona"],
            "id_atleta_2": atleta_2["id_persona"],
            "id_competencia": competencia["id_competencia"],
            "fecha": fake.date_this_year(),
            "hora": fake.time(),
            "resultado": random.choice(["Victoria Atleta 1", "Victoria Atleta 2"])
        }
        combates.append(combate)
    return combates

# Guardar en CSV
def guardar_csv(datos, directorio, nombre_archivo):
    df = pd.DataFrame(datos)
    filepath = os.path.join(directorio, nombre_archivo)
    df.to_csv(filepath, index=False, sep=";")
    print(f"Archivo '{nombre_archivo}' generado en {directorio}.")

# Generar todos los datos
def generar_todos():
    tamanos = [1000, 10000, 100000, 1000000]

    for tamano in tamanos:
        # Generar personas (triple de atletas, jueces y entrenadores combinados)
        num_personas = tamano * 3
        personas = generar_personas(num_personas)
        guardar_csv(personas, output_dirs["personas"], f"personas_{num_personas}.csv")

        # Dividir personas entre jueces, atletas y entrenadores
        num_jueces = tamano
        num_atletas = tamano
        num_entrenadores = tamano

        jueces = generar_jueces(num_jueces, personas[:num_jueces])
        guardar_csv(jueces, output_dirs["jueces"], f"jueces_{tamano}.csv")

        atletas = generar_atletas(num_atletas, personas[num_jueces:num_jueces + num_atletas])
        guardar_csv(atletas, output_dirs["atletas"], f"atletas_{tamano}.csv")

        entrenadores = generar_entrenadores(num_entrenadores, personas[num_jueces + num_atletas:num_jueces + num_atletas + num_entrenadores])
        guardar_csv(entrenadores, output_dirs["entrenadores"], f"entrenadores_{tamano}.csv")

        # Generar equipos
        num_equipos = tamano // 10  # Ejemplo: 1 equipo por cada 10 personas
        equipos = generar_equipos(num_equipos)
        guardar_csv(equipos, output_dirs["equipos"], f"equipos_{tamano}.csv")

        # Generar competencias
        competencias = generar_competencias(tamano)
        guardar_csv(competencias, output_dirs["competencias"], f"competencias_{tamano}.csv")

        # Generar combates
        combates = generar_combates(tamano, atletas, jueces, competencias)
        guardar_csv(combates, output_dirs["combates"], f"combates_{tamano}.csv")

if __name__ == "__main__":
    generar_todos()
