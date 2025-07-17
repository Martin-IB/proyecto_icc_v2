import serial
import serial.tools.list_ports
import requests
import random
import time

API_URL = "http://3.132.200.37:8000/lectura/"
#API_URL = "http://localhost:8000/lectura/"
BIORREACTOR_ID = 1
SENSOR_ID = 1

def encontrar_puerto():
    puertos_disponibles = serial.tools.list_ports.comports()
    return [p.device for p in puertos_disponibles]

def conectar_sensor():
    while True:
        for nombre_puerto in encontrar_puerto():
            try:
                return serial.Serial(nombre_puerto, 115200, timeout=4)
            except serial.SerialException:
                time.sleep(1)
        time.sleep(2)

puerto = conectar_sensor()

while True:
    try:
        if not puerto.is_open:
            puerto = conectar_sensor()
        linea = puerto.readline().decode('utf-8').strip()
        if "," in linea:
            partes = linea.split(",")
            temperatura_real = float(partes[0])
            humedad = float(partes[1])
            if temperatura_real < 25:
                diferencia = 27 - temperatura_real
                ruido = random.uniform(-0.35, 0.35)
                temperatura_simulada = temperatura_real + diferencia + ruido
            else:
                temperatura_simulada = temperatura_real
            payload = {
                "temperatura": round(temperatura_simulada, 2),
                #"temperatura": round(temperatura_real, 2),
                "humedad": round(humedad, 2),
                "Biorreactor_idBiorreactor": BIORREACTOR_ID,
                "Sensores_idSensores": SENSOR_ID
            }
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"{data['temperatura']}°C | {data['humedad']}% | {data['estado_ambiente']}")
            else:
                print(f"{response.status_code}: {response.text}")
    except (serial.SerialException, OSError):
        puerto = conectar_sensor()
    except Exception as e:
        print("Error:", e)
