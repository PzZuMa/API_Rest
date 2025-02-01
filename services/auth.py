from services import config
import requests

# Función para obtener el token de autenticación
def get_token():
    url = f"{config.BASE_URL}/login"
    data = {"apikey": config.API_KEY}
    response = requests.post(url, json=data) # Realiza una solicitud POST al endpoint de login con los datos de autenticación
    if response.status_code == 200: # Verifica si la solicitud fue exitosa
        return response.json()["data"]["token"] # Obtiene el token de la solicitud
    else:
        print(f"Failed to get token. Status code: {response.status_code}, Response: {response.text}")
        raise Exception(f"Error en la solicitud: {response.status_code}")