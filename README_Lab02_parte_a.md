# Sistema de Captura de Dados Climáticos via MQTT - Parte A

## 🌟 Sobre o Projeto

Esta parte do projeto implementa a captura de dados climáticos em tempo real utilizando MQTT e armazenamento em banco de dados de série temporal (InfluxDB). O sistema utiliza Node-RED para orquestração dos fluxos de dados IoT.

### 📋 Funcionalidades Principais

- 🌡️ **Dados em Tempo Real**: Captura de dados climáticos via MQTT
- 📊 **Banco de Série Temporal**: Armazenamento no InfluxDB para análise histórica
- 🔄 **Node-RED**: Orquestração de fluxos e integrações

### 🏗️ Arquitetura do Sistema

```
[Sensores IoT] → [MQTT Broker] → [Node-RED] → [InfluxDB]
```

## 📋 Pré-requisitos

### Software Necessário

- [Docker](https://docs.docker.com/get-docker/) (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0+)
- Git

### Contas e APIs Necessárias

- **MQTT Broker**: Pode usar um broker público ou privado

## Configuração do EC2 AWS

**Proteger chave**

```bash
chmod 400 minha-chave-docker.pem
```

**acesso via ssh**

```bash
ssh -i "minha-chave-docker.pem" ec2-user@SEU_IP_PUBLICO_AQUI
```

**Atualiza os pacotes do sistema**

```bash
sudo yum update -y
```

**Instala o docker**

```bash
sudo yum install docker -y
```

**Iniciar o docker**

```bash
sudo service docker start
```

**Add User ao grupo do Docker**

```bash
sudo usermod -a -G docker ec2-user
```

**Sai do servidor**

```bash
exit
```

**Docker compose**

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m)" -o /usr/libexec/docker/cli-plugins/docker-compose
sudo chmod +x /usr/libexec/docker/cli-plugins/docker-compose
docker compose version
```

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/Fernando-EngComputacao/lab_02_ufg_2055.git
cd lab_02_ufg_2055
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo `.env` e configure as variáveis relacionadas ao MQTT e InfluxDB:

```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:

- MQTT_BROKER_HOST
- MQTT_BROKER_PORT
- INFLUXDB_URL
- INFLUXDB_TOKEN
- INFLUXDB_ORG
- INFLUXDB_BUCKET

### 3. Iniciar os Serviços

```bash
docker-compose up -d
```

### 4. Acessar Node-RED

Abra o navegador em `http://localhost:1880` (ou o IP do seu servidor).

### 5. Importar o Fluxo

No Node-RED, importe o arquivo `template/01_Lab02_parte_a.json` para carregar o fluxo de captura de dados via MQTT.

## 📖 Como Usar

1. Configure os sensores IoT para publicar dados no tópico MQTT `ufg/2025/weather`.
2. Os dados serão capturados pelo Node-RED e armazenados no InfluxDB.
3. Monitore os dados através do painel de debug no Node-RED ou consultas diretas ao InfluxDB.

## 🐍 Configuração do Publicador Python para MQTT

Para alimentar o MQTT com dados dos sensores, você pode usar um script Python que publica dados climáticos simulados ou reais. Siga os passos abaixo para configurar uma instância Python que roda como serviço no sistema.

### 🗂️ 1. Criar Pasta do Projeto

```bash
mkdir pyhton_ufg
cd pyhton_ufg
```

### 📝 2. Criar o Arquivo Python

Crie o arquivo `weather.py` com o código para publicar dados no MQTT. 

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

Node-RED
```
node-red-contrib-aedes
node-red-contrib-chartjs
node-red-contrib-chartjs-line-alt
node-red-contrib-evolution-api
node-red-contrib-influxdb
node-red-node-telegrambot
node-red-contrib-telegrambot
node-red-contrib-ui-artless-gauge
node-red-contrib-ui-reef
node-red-dashboard
node-red-node-mysql
sense-rsa
```

Function: Tratamento Influx

```
msg.payload = [
    {
        measurement: "UFG-2025",
        fields: {
            temperatura: msg.payload.temperatura_c,
            sensacao_termica: msg.payload.sensacao_termica_c,
            umidade: msg.payload.umidade_percent

        },
        tags: {
            sendorID: 1,
            location: "Goiania GO"
        }
    }
];

return msg;

```

## �🔧 Configurações Adicionais

- Ajuste os tópicos MQTT conforme necessário.
- Configure retenção de dados no InfluxDB para otimizar armazenamento.