import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

if __name__ == '__main__':
    API_KEY = "7da18426-1bdc-464b-89e1-fedba6b544fa"
    BASE_URL = "https://api4.thetvdb.com/v4"

    def get_token():
        url = f"{BASE_URL}/login"
        data = {"apikey": API_KEY}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["data"]["token"]
        else:
            print(f"Failed to get token. Status code: {response.status_code}, Response: {response.text}")
            raise Exception(f"Error en la solicitud: {response.status_code}")

    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    def get_dragonball_series() -> List[Dict]:
        """
        Obtiene todas las series de Dragon Ball.
        Filtra cuidadosamente para evitar falsos positivos.
        """
        try:
            response = requests.get(
                f"{BASE_URL}/search",
                params={
                    "query": "Dragon Ball",
                    "type": "series"
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()['data']

            # return data
            # Filtrar solo las series genuinas de Dragon Ball
            return [series for series in data
                    if "Dragon Ball" in series['name']
                    and not any(excluded in series['name'].lower()
                                for excluded in ['parody', 'fanfilm'])]

        except requests.RequestException as e:
            print(f"Error al obtener las series: {e}")
            return []

    def get_oldest_poster_series_1986() -> Optional[Dict]:
        """
        Obtiene la serie más antigua registrada de 1986.
        Devuelve un diccionario con la información de la serie o None si no se encuentra.
        """
        try:
            response = requests.get(
                f"{BASE_URL}/series/filter",
                params={
                    "year": 1986,
                    "sort": "firstAired"
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()['data']

            # for serie in data:
            #     print(serie['name'],serie['firstAired'], serie['image'])


            return data

        except requests.RequestException as e:
            print(f"Error al obtener la serie: {e}")
            return None

    def fecha_emision():
        try:
            response = requests.get(
                f"{BASE_URL}/search",
                params={
                    "query": "Saga del Ejército de la Patrulla Roja",
                    "type": "series"
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()['data']

            return data

        except requests.RequestException as e:
            print(f"Error al obtener las series: {e}")
            return []

    dragonballseries = get_dragonball_series()
    print("Series de Dragon Ball: ", len(dragonballseries))
    posterantiguo = get_oldest_poster_series_1986()
    # print("Poster más antiguo de 1986: ", posterantiguo['image'])
    EjércitodelaPatrullaRoja = fecha_emision()
    print("Fecha de emisión de la Saga del Ejército de la Patrulla Roja: ", EjércitodelaPatrullaRoja)


    with open('SeriesDragonBall.json', 'w', encoding='utf-8') as f:
        json.dump(dragonballseries, f, ensure_ascii=False, indent=4)
    with open('PosterViejo.json', 'w', encoding='utf-8') as f:
        json.dump(posterantiguo, f, ensure_ascii=False, indent=4)

