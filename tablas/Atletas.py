from faker import Faker
import random
import os
import pandas as pd

fake = Faker()

# Directorios de salida
output_dirs = {
    "equipos": "csv/Equipos",
    "competencias": "csv/Competencias",
    "combates": "csv/Combates",
}

# Crear directorios
for key, path in output_dirs.items():
    os.makedirs(path, exist_ok=True)

# Generar equipos
def generar_datos_equipo(num_equipos):
    equipos = []
    for i in range(1, num_equipos + 1):
        equipo = {
            "ID_equipo": i,
            "nombre": f"Equipo {i}",
            "ID_arte_marcial": random.randint(1, 5),  # 5 artes marciales fijas
        }
        equipos.append(equipo)
    return equipos

# Generar competencias
def generar_datos_competencia(num_competencias):
    competencias = []
    for i in range(1, num_competencias + 1):
        competencia = {
            "ID_competencia": i,
            "nombre": f"Competencia {i}",
            "fecha_inicio": fake.date_this_year(),
            "fecha_fin": fake.date_this_year(),
            "lugar": fake.city(),
        }
        competencias.append(competencia)
    return competencias

# Generar combates
def generar_datos_combate(num_combates, atleta_ids, juez_ids, competencia_ids):
    combates = []
    for i in range(1, num_combates + 1):
        combate = {
            "ID_combate": i,
            "ID_juez": random.choice(juez_ids),
            "resultado": random.choice(["Victoria Atleta 1", "Victoria Atleta 2"]),
            "fecha": fake.date_this_year(),
            "hora": fake.time(),
            "ID_competencia": random.choice(competencia_ids),
            "ID_atleta_1": random.choice(atleta_ids),
            "ID_atleta_2": random.choice(atleta_ids),
        }
        # Asegurarse de que no sean el mismo atleta
        while combate["ID_atleta_1"] == combate["ID_atleta_2"]:
            combate["ID_atleta_2"] = random.choice(atleta_ids)
        combates.append(combate)
    return combates

# Guardar datos en CSV
def guardar_csv(datos, directorio, nombre_archivo):
    df = pd.DataFrame(datos)
    filepath = os.path.join(directorio, nombre_archivo)
    df.to_csv(filepath, index=False, sep=";")
    print(f"Archivo {nombre_archivo} generado en {directorio}.")

# Generar datos para todas las tablas restantes
def generar_tablas_restantes():
    tamanos = [1000, 10000, 100000, 1000000]

    for tamano in tamanos:
        # Generar equipos (escalar con el tamaño base)
        equipos = generar_datos_equipo(tamano // 10)  # Ejemplo: 1 equipo por cada 10 personas
        guardar_csv(equipos, output_dirs["equipos"], f"equipos_{len(equipos)}.csv")

        # Generar competencias (escalar con el tamaño base)
        competencias = generar_datos_competencia(tamano // 100)  # Ejemplo: 1 competencia por cada 100 personas
        guardar_csv(competencias, output_dirs["competencias"], f"competencias_{len(competencias)}.csv")

        # Cargar atletas y jueces ya generados
        atletas = pd.read_csv(f"csv/Atletas/atletas_{tamano}.csv", sep=";")
        jueces = pd.read_csv(f"csv/Jueces/jueces_{tamano}.csv", sep=";")

        # Generar combates
        combates = generar_datos_combate(
            tamano // 2,  # Ejemplo: 1 combate por cada 2 personas
            atletas["ID_persona"].tolist(),
            jueces["ID_persona"].tolist(),
            range(1, len(competencias) + 1),
        )
        guardar_csv(combates, output_dirs["combates"], f"combates_{len(combates)}.csv")

if __name__ == "__main__":
    generar_tablas_restantes()
