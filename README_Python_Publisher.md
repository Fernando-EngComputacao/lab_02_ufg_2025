# Publicador Python para MQTT - Alimentação de Dados Climáticos

Este documento explica como configurar um script Python que publica dados climáticos simulados ou reais no broker MQTT, alimentando o sistema de captura de dados da Parte A.

## 🐍 Configuração do Publicador Python para MQTT

Para alimentar o MQTT com dados dos sensores, você pode usar um script Python que publica dados climáticos simulados ou reais. Siga os passos abaixo para configurar uma instância Python que roda como serviço no sistema.

### 🗂️ 1. Criar Pasta do Projeto

```bash
mkdir pyhton_ufg
cd pyhton_ufg
```

### 📝 2. Criar o Arquivo Python

Crie o arquivo `weather.py` com o código para publicar dados no MQTT. Exemplo básico:

```python
import paho.mqtt.client as mqtt
import json
import time
import random
import requests

# Configurações MQTT
MQTT_BROKER = "broker.hivemq.com"  # ou seu broker
MQTT_PORT = 1883
MQTT_TOPIC = "ufg/2025/weather"

# Função para obter dados climáticos da API (exemplo com OpenWeatherMap)
def get_weather_data():
    # Substitua pela sua API key e cidade
    api_key = "YOUR_API_KEY"
    city = "Goiania"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return {
        "temperatura": data["main"]["temp"],
        "umidade": data["main"]["humidity"],
        "sensacao_termica": data["main"]["feels_like"]
    }

# Ou simular dados
def simulate_weather_data():
    return {
        "temperatura": round(random.uniform(20, 35), 2),
        "umidade": random.randint(40, 80),
        "sensacao_termica": round(random.uniform(18, 38), 2)
    }

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    # data = get_weather_data()  # Para dados reais
    data = simulate_weather_data()  # Para simulação
    payload = json.dumps(data)
    client.publish(MQTT_TOPIC, payload)
    print(f"Publicado: {payload}")
    time.sleep(60)  # Publica a cada 1 minuto
```

### 🛠️ 3. Instalar Python e Dependências

```bash
sudo yum update -y
sudo yum install python3-pip -y
pip install paho-mqtt requests
```

### 🔍 Descobrir Caminhos Necessários

Antes de configurar o serviço, é importante identificar os caminhos corretos para o Python e para o arquivo do script:

1. **Caminho do Python 3**:

   ```bash
   which python3
   ```

   Este comando retorna o caminho completo do interpretador Python 3 no sistema.

2. **Caminho do Arquivo Python (`weather.py`)**:

   Navegue até a pasta do projeto e execute:

   ```bash
   pwd
   ```

   Este comando retorna o caminho completo da pasta onde o arquivo `weather.py` está localizado.

### ⚙️ 4. Configurar o Serviço Systemd

Crie o arquivo de configuração do serviço:

```bash
sudo nano /etc/systemd/system/weather-service.service
```

Cole o seguinte conteúdo (ajuste os caminhos conforme necessário):

```ini
[Unit]
Description=Script Python para Publicar Dados Climáticos no MQTT
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/pyhton_ufg
ExecStart=/usr/bin/python3 /home/ec2-user/pyhton_ufg/weather.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Notas**:
- Para descobrir o caminho do Python 3: `which python3`
- Para obter o caminho da pasta do projeto: navegue até ela e execute `pwd`

### 🚀 5. Gerenciar o Serviço

Recarregue o systemd:

```bash
sudo systemctl daemon-reload
```

Para iniciar o serviço automaticamente com o servidor:

```bash
sudo systemctl enable weather-service.service
```

Para iniciar o serviço agora:

```bash
sudo systemctl start weather-service.service
```

Para parar o serviço:

```bash
sudo systemctl stop weather-service.service
```

Para reiniciar o serviço:

```bash
sudo systemctl restart weather-service.service
```

Para verificar o status:

```bash
sudo systemctl status weather-service.service
```

Este documento complementa o [README da Parte A](README_Lab02_parte_a.md) com instruções específicas para a publicação de dados via Python.