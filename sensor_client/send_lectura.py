import serial
import requests
import random
import json

# Configura tu puerto serial
puerto = serial.Serial('COM5', 115200, timeout=4)

# Configura la URL del endpoint FastAPI
API_URL = "http://18.188.154.229:8000/lectura/"

# IDs fijos de prueba (asegúrate que existan en tu DB)
BIORREACTOR_ID = 1
SENSOR_ID = 1

print("Esperando datos del sensor...\n")

while True:
    try:
        linea = puerto.readline().decode('utf-8').strip()

        if "," in linea:
            partes = linea.split(",")
            temperatura_real = float(partes[0])
            humedad = float(partes[1])

            # Simulación ajustada si es menor a 25 °C
            if temperatura_real < 25:
                diferencia = 27 - temperatura_real
                ruido = random.uniform(-1.15, 1.5)  # ruido realista
                temperatura_simulada = temperatura_real + diferencia + ruido
            else:
                temperatura_simulada = temperatura_real

            payload = {
                "temperatura": round(temperatura_simulada, 2),
                "humedad": round(humedad, 2),
                "Biorreactor_idBiorreactor": BIORREACTOR_ID,
                "Sensores_idSensores": SENSOR_ID
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                print(f" Lectura enviada | Temp: {data['temperatura']}°C | Hum: {data['humedad']}% | Estado: {data['estado_ambiente']}")
            else:
                print(f" Error {response.status_code}: {response.text}")

    except Exception as e:
        print("Error procesando datos:", e)
