import requests

response = requests.get("http://3.132.200.37:8000/lectura/")
for row in response.json():
    print(f"ID: {row['idLectura_sensores']} | Temp: {row['temperatura']} | Hum: {row['humedad']} | Estado: {row['estado_ambiente']} | Fecha: {row['fecha']}")
