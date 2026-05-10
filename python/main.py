import requests
from datetime import datetime, UTC

# La URL de tu compañero de Backend
API_ENDPOINT = "http://vlb-cd06317a-3468-4e5b-b751-5429ce5ca5ba.vultrlb.com/road-incidents"

print("🚀 Iniciando TEST de conexión con la API...")

# Creamos un bache falso en el centro de Barcelona
payload_prueba = {
    "image_url": "base64_de_prueba_simulando_una_foto_cortita",
    "gps": {
        "latitude": 41.3851,
        "longitude": 2.1734
    },
    "timestamp": datetime.now(UTC).isoformat(),
    "type_of_damage": "bache",
    "num_of_potholes": 1,
    "num_of_signals": 0
}

try:
    print(f"📡 Enviando POST a: {API_ENDPOINT}")
    print(f"📦 Datos enviados: {payload_prueba}\n")
    
    # Hacemos la petición con un límite de 10 segundos para que no se cuelgue
    response = requests.post(API_ENDPOINT, json=payload_prueba, timeout=10)
    
    print("-" * 40)
    print(f"HTTP Status Code : {response.status_code}")
    
    # Intentamos leer la respuesta del servidor para ver si se queja de algún campo
    try:
        print(f"Respuesta Server : {response.json()}")
    except:
        print(f"Respuesta Server : {response.text}")
    print("-" * 40)
        
    if response.status_code in [200, 201]:
        print("\n✅ ¡ÉXITO! La API funciona perfectamente y se ha tragado el bache.")
        print("El problema estaba en el botón físico de la placa.")
    elif response.status_code == 422:
        print("\n⚠️ ERROR 422 (Unprocessable Entity).")
        print("La API funciona, pero no le gusta el formato del JSON. Revisad los tipos de datos en el Backend (FastAPI).")
    else:
        print("\n⚠️ ERROR DEL SERVIDOR.")
        print("Dile a tu compañero de Backend que revise los logs de Vultr.")
        
except requests.exceptions.Timeout:
    print("\n❌ ERROR: Timeout. La API no responde (ha tardado más de 10 segundos). El servidor podría estar apagado o bloqueando la IP.")
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Connection Error. No se ha podido alcanzar el servidor. ¿Está bien escrita la URL o le falta el puerto?")
except Exception as e:
    print(f"\n❌ ERROR CRÍTICO DESCONOCIDO: {e}")