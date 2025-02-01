from services import config
import requests

# Función para obtener todas las series de Dragon Ball.
def get_dragonball_series(headers):
    try:
        # Realiza una solicitud GET al endpoint de búsqueda con los parámetros especificados.
        response = requests.get(
            f"{config.BASE_URL}/search",
            params={
                "query": "Dragon Ball",
                "type": "series"
            },
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        series = response.json()['data']  # Obtiene los datos de la solicitud

        series_dragonball = []

        # Filtra las series que contienen "Dragon Ball" en su nombre y cuyo idioma principal es japonés.
        for elemento in series:
            if ("Dragon Ball" in elemento['name'] or "ドラゴンボール" in elemento['name']) and elemento[
                'primary_language'] == "jpn":
                series_dragonball.append(elemento)

        return series_dragonball

    except requests.RequestException as e:
        print(f"Error al obtener las series: {e}")
        return []


# Función para obtener la fecha de emisión del primer episodio de la tercera temporada de una serie
def fecha_emision(id_serie, headers):
    try:
        # Realiza una solicitud GET al endpoint de series extendido con el ID de la serie
        response = requests.get(
            f"{config.BASE_URL}/series/{id_serie}/extended",
            params={
                "season": 3
            },
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        datos_serie = response.json()['data']  # Obtiene los datos de la solicitud

        seasons = datos_serie['seasons']
        id_season = None

        # Encuentra el ID de la tercera temporada
        for season in seasons:
            if season['number'] == 3:
                id_season = season['id']

        # Realiza una solicitud GET al endpoint de temporadas extendido con el ID de la temporada
        response = requests.get(
            f"{config.BASE_URL}/seasons/{id_season}/extended",
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        episodios_temporada_3 = response.json()['data']['episodes']  # Obtiene los datos de la solicitud

        primer_episodio = episodios_temporada_3[0]  # Obtiene el primer episodio

        return primer_episodio

    except requests.RequestException as e:
        print(f"Error al obtener las series: {e}")
        return []


# Función para obtener la información del actor que interpretó a Goku en Dragonball Evolution
def actor_goku(headers):
    try:
        # Realiza una solicitud GET al endpoint de búsqueda con los parámetros especificados
        response = requests.get(
            f"{config.BASE_URL}/search",
            params={
                "query": "Dragonball Evolution",
                "type": "movie"
            },
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        db_evolution = response.json()['data']  # Obtiene los datos de la solicitud

        id_movie = db_evolution[0]['tvdb_id']  # Obtiene el ID de la película

        # Realiza una solicitud GET al endpoint de películas extendido con el ID de la película
        response = requests.get(
            f"{config.BASE_URL}/movies/{id_movie}/extended",
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        info_personajes = response.json()['data']['characters']  # Obtiene los datos de la solicitud

        id_actor = None
        # Encuentra el ID del actor que interpretó a Goku
        for personaje in info_personajes:
            if personaje['name'] == "Goku":
                id_actor = personaje['peopleId']

        # Realiza una solicitud GET al endpoint de personas extendido con el ID del actor
        response = requests.get(
            f"{config.BASE_URL}/people/{id_actor}/extended",
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        info_actor = response.json()['data']  # Obtiene los datos de la solicitud

        return info_actor

    except requests.RequestException as e:
        print(f"Error al obtener las series: {e}")
        return []


# Función para obtener la película con mejor score del año 2005
def mejor_peli_ano(headers):
    try:
        # Realiza una solicitud GET al endpoint de búsqueda con los parámetros especificados
        response = requests.get(
            f"{config.BASE_URL}/search",
            params={
                "query": "La guerra de los mundos",
                "type": "movie"
            },
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        query_pelicula = response.json()['data']  # Obtiene los datos de la solicitud

        ano_pelicula = None

        # Encuentra el año de la película "La guerra de los mundos"
        for pelis in query_pelicula:
            if pelis['translations']['spa'] == "La guerra de los mundos":
                ano_pelicula = pelis['year']

        # Realiza una solicitud GET al endpoint de búsqueda con los parámetros especificados
        response = requests.get(
            f"{config.BASE_URL}/search",
            params={
                "query": ano_pelicula,
                "type": "movie",
                "year": ano_pelicula,
                "contry": "usa"
            },
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        peliculas_ano_2005 = response.json()['data']  # Obtiene los datos de la solicitud

        peliculas_score = []
        # Obtiene los datos extendidos de cada película y los almacena en una lista
        for pelicula in peliculas_ano_2005:
            response = requests.get(
                f"{config.BASE_URL}/movies/{pelicula['tvdb_id']}/extended",
                headers=headers
            )
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            datos_pelicula = response.json()['data']  # Obtiene los datos de la solicitud

            peliculas_score.append({
                "id": datos_pelicula['id'],
                "nombre": datos_pelicula['name'],
                "puntuacion": datos_pelicula['score']
            })

        # Encuentra la película con la mejor puntuación
        mejor_score_ano = max(peliculas_score, key=lambda x: x['puntuacion'])

        # Realiza una solicitud GET al endpoint de películas extendido con el ID de la mejor película
        response = requests.get(
            f"{config.BASE_URL}/movies/{mejor_score_ano['id']}/extended",
            headers=headers
        )
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        mejor_pelicula = response.json()['data']  # Obtiene los datos de la solicitud

        return mejor_pelicula

    except requests.RequestException as e:
        print(f"Error al obtener las series: {e}")
        return []