import paho.mqtt.client as mqtt
import requests
import json
import time
from datetime import datetime, timezone  # <-- 1. ALTERAÇÃO: Importar timezone também
from zoneinfo import ZoneInfo           # <-- 1. ALTERAÇÃO: Importar ZoneInfo

# --- 1. Configurações ---
# A chave de API está inserida diretamente no código conforme solicitado.
API_KEY = "807dcc76bb1575edaa655d5bae20a8e7" # Lembre-se que esta chave de exemplo é inválida

# Configurações do MQTT Broker e OpenWeatherMap
BROKER_ADDRESS = "broker.mqtt-dashboard.com"
BROKER_PORT = 1883
MQTT_TOPIC = "ufg/2025/weather"
API_URL_BASE = "https://api.openweathermap.org/data/2.5/weather"
CIDADE = "Goiânia,br"
# <-- 2. ALTERAÇÃO: Definir o fuso horário de Brasília
BR_TIMEZONE = ZoneInfo("America/Sao_Paulo")


# --- 2. Funções Auxiliares ---

# <-- 3. ALTERAÇÃO: Atualizar a função para converter fusos horários
def formatar_timestamp_para_hora_br(timestamp):
    """Converte um timestamp Unix (UTC) para uma string de hora 'HH:MM:SS' no fuso de Brasília."""
    if timestamp:
        # Cria um objeto datetime a partir do timestamp, ciente de que é UTC
        utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        # Converte o tempo UTC para o fuso horário de Brasília
        br_time = utc_time.astimezone(BR_TIMEZONE)
        # Retorna a string formatada
        return br_time.strftime('%H:%M:%S')
    return None

def get_weather_data(api_key, cidade):
    """Busca os dados do clima na API e retorna um dicionário formatado."""
    params = {'q': cidade, 'APPID': api_key, 'units': 'metric', 'lang': 'pt_br'}
    try:
        response = requests.get(API_URL_BASE, params=params)
        response.raise_for_status()
        data = response.json()
        payload_formatado = {
            "cidade": data.get("name"),
            "temperatura_c": data["main"].get("temp"),
            "sensacao_termica_c": data["main"].get("feels_like"),
            "umidade_percent": data["main"].get("humidity"),
            "clima_desc": data["weather"][0].get("description"),
            # <-- 4. ALTERAÇÃO: Usar a nova função com conversão de fuso
            "amanhecer": formatar_timestamp_para_hora_br(data["sys"].get("sunrise")),
            "anoitecer": formatar_timestamp_para_hora_br(data["sys"].get("sunset")),
            "timestamp_unix": data.get("dt"),
        }
        return payload_formatado
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Erro HTTP ao buscar clima: {http_err}")
        if response.status_code == 401: print("   -> A API Key no código pode ser inválida ou ter expirado.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado ao buscar clima: {e}")
    return None

def on_connect(client, userdata, flags, rc):
    """Callback de conexão."""
    if rc == 0:
        print("✅ Conectado ao Broker MQTT com sucesso!")
    else:
        print(f"Falha ao conectar, código de retorno: {rc}\n")

# --- 3. Lógica Principal ---

client = mqtt.Client(client_id=f"ufg_weather_publisher_{int(time.time())}")
client.on_connect = on_connect

print(f"Conectando ao broker {BROKER_ADDRESS}...")
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
client.loop_start()

try:
    while True:
        print("\n------------------------------")
        weather_payload = get_weather_data(API_KEY, CIDADE)

        if weather_payload:
            message = json.dumps(weather_payload, ensure_ascii=False)
            result = client.publish(MQTT_TOPIC, message)

            if result[0] == 0:
                print(f"🛰️  Mensagem publicada com sucesso no tópico:")
                print(f"   '{MQTT_TOPIC}'")
                print(f"   Payload: {message}")
            else:
                print(f"⚠️  Falha ao enviar mensagem para o tópico '{MQTT_TOPIC}'")
        else:
            print("Não foi possível obter os dados do clima. Nova tentativa em 5 segundos.")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n\n🛑 Publicação interrompida pelo usuário.")
finally:
    print("Desconectando do broker...")
    client.loop_stop()
    client.disconnect()
    print("Cliente desconectado.")