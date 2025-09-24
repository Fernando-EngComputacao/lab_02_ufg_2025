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

## 🔧 Configurações Adicionais

- Ajuste os tópicos MQTT conforme necessário.
- Configure retenção de dados no InfluxDB para otimizar armazenamento.</content>
<parameter name="filePath">c:\Users\carri\Documents\IoT\Lab_02\README_Lab02_parte_a.md