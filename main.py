import requests
import json
from services import auth, TVDB_Services, config

def to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # Obtiene el token de autenticación
    token = auth.get_token()

    # Configura los encabezados de la solicitud con el token de autenticación
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # TAREA 1 - Obtener todas las series de Dragon Ball oficiales.

    dragonballseries = TVDB_Services.get_dragonball_series(headers)
    print(f"TAREA 1\n\t-> Hay {len(dragonballseries)} series originales de Dragon Ball en la base de datos.\n")

    db_antigua = None

    # TAREA 2 - Buscar el póster de la serie original de Dragon Ball (1986).

    for serie in dragonballseries:
        if serie['year'] == "1986":
            db_antigua = serie
            print(f"TAREA 2\n\t-> Póster de la serie original de Dragon Ball(1986): {serie['image_url']}\n")

    # TAREA 3 - Obtener la fecha de emisión del primer episodio de la tercera temporada de la
    # serie original de Dragon Ball con su nombre y descripción en español.

    fecha_emision_3season = TVDB_Services.fecha_emision(db_antigua['tvdb_id'], headers)

    id_episodio = fecha_emision_3season['id']

    # Realiza una solicitud para obtener la traducción al español del primer episodio de la tercera temporada
    response = requests.get(
        f"{config.BASE_URL}/episodes/{id_episodio}/translations/spa",
        headers=headers
    )
    response.raise_for_status()
    datos_episodio = response.json()['data']

    print(f"TAREA 3\n\t-> La fecha de emisión del primer episodio de la tercera temporada "
          f"de Dragon Ball es: '{fecha_emision_3season['aired']}' con nombre '{datos_episodio['name']}' y "
          f"con descripcion '{datos_episodio['overview']}'\n")

    # TAREA 4 - Obtener la información del actor que interpretó a Goku en Dragonball Evolution
    # junto con todas sus participaciones en series y películas.

    actor_dbevolution = TVDB_Services.actor_goku(headers)
    print(f"TAREA 4\n\t-> El nombre del actor de Goku en la pelicula Dragon Ball Evolution es "
          f"'{actor_dbevolution['name']}' y ha estado en {len(actor_dbevolution['characters'])} series y peliculas.\n")

    # TAREA 5 - Obtener la pelicula con mejor score del año en el que salió la película “La guerra de los mundos”.

    mejor_peli = TVDB_Services.mejor_peli_ano(headers)
    print(f"TAREA 5\n\t-> La mejor pelicula del año 2005 es '{mejor_peli['name']}' con "
          f"una puntuacion de {mejor_peli['score']}.")

    # Guardamos los resultados en archivos JSON
    to_json(dragonballseries, 'resultado/SeriesDragonBall.json')
    to_json(fecha_emision_3season, 'resultado/PriperEpisodio3Temporada.json')
    to_json(actor_dbevolution, 'resultado/ActorDBEvolution.json')
    to_json(mejor_peli, 'resultado/MejorPeliAño.json')

