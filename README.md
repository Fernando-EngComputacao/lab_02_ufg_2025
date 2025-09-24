# Sistema de Assistente Telegram com Dados Climáticos - Goiânia

Este README está dividido em duas partes para facilitar o desenvolvimento e teste incremental:

- **[Parte A: Captura de Dados via MQTT](README_Lab02_parte_a.md)** - Foca na coleta e armazenamento de dados climáticos.
- **[Parte B: Assistente Telegram com IA](README_Lab02_parte_b.md)** - Foca no bot interativo e processamento com IA.
- **[Fundamentos e Tecnologias Utilizadas](README_Fundamentos.md)** - Para entender melhor os conceitos e tecnologias utilizados neste projeto, consulte o documento.


## 🌟 Sobre o Projeto

Este projeto implementa um assistente inteligente no Telegram que fornece recomendações personalizadas de locais para visitar em Goiânia, baseando-se em dados climáticos em tempo real. O sistema utiliza uma arquitetura IoT completa com MQTT, banco de dados de série temporal, e integração com IA (Google Gemini).

### 📋 Funcionalidades Principais

- 🤖 **Assistente Telegram**: Bot interativo para receber consultas dos usuários
- 🌡️ **Dados em Tempo Real**: Captura de dados climáticos via MQTT
- 📊 **Banco de Série Temporal**: Armazenamento no InfluxDB para análise histórica
- 🧠 **IA Integrada**: Processamento com Google Gemini para respostas contextualizadas
- 🏢 **API WhatsApp**: Evolution API para comunicação
- 🔄 **Node-RED**: Orquestração de fluxos e integrações

### 🏗️ Arquitetura do Sistema

```
[Sensores IoT] → [MQTT Broker] → [Node-RED] → [InfluxDB]
                                      ↓
[Telegram Bot] ← [Gemini AI] ← [Evolution API]
```

## 📋 Pré-requisitos

### Software Necessário

- [Docker](https://docs.docker.com/get-docker/) (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0+)
- Git

### Contas e APIs Necessárias

- **Telegram Bot Token**: Criar bot via @BotFather
- **Google Gemini API Key**: Conta no Google Cloud Platform
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
git clone https://github.com/Fernando-EngComputacao/node-red-whatsapp.git
cd node-red-whatsapp
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo `.env` e configure as variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Evolution API
SERVER_TYPE=http
SERVER_PORT=8080
SERVER_URL=http://localhost:8080

# Database
DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI='postgresql://user:pass@postgres:5432/evolution_db?schema=evolution_api'

# Outras configurações...
```

### 3. Inicializar os Serviços

```bash
docker-compose up -d
```

### 4. Verificar Status dos Serviços

```bash
docker-compose ps
```

Todos os serviços devem estar com status "Up".

## 🔧 Configuração Detalhada dos Serviços

### 🐳 Docker Compose - Visão Geral dos Serviços

O projeto utiliza os seguintes serviços:

- **Redis**: Cache e sessões (porta 6379)
- **PostgreSQL**: Banco de dados principal (porta 5432)
- **Evolution API**: API WhatsApp (porta 8080)
- **Node-RED**: Orquestração de fluxos (porta 1880)
- **InfluxDB**: Banco de dados de série temporal (porta 8086)

### 📱 Configuração do Telegram

#### Passo 1: Criar Bot no Telegram

1. Abra o Telegram e procure por `@BotFather`
2. Digite `/newbot`
3. Escolha um nome para seu bot (ex: "GoiâniaTurismoBot")
4. Escolha um username único (ex: "goiania_turismo_bot")
5. Salve o **token** fornecido

#### Passo 2: Configurar no Node-RED

1. Acesse o Node-RED: `http://localhost:1880`
2. Instale os nós do Telegram:
   - Vá em **Menu** → **Manage Palette** → **Install**
   - Procure por `node-red-contrib-telegrambot`
   - Clique em **Install**

3. Configure o nó Telegram:
   - Arraste um nó **Telegram receiver** para o workspace
   - Duplo-clique para configurar
   - Clique no lápis ao lado de "Bot"
   - Cole o **Token** do seu bot
   - Adicione um nome para a configuração
   - Clique em **Add** e depois **Done**

#### Exemplo de Fluxo Telegram no Node-RED

```json
[
    {
        "id": "telegram_receiver",
        "type": "telegram receiver",
        "name": "Receber Mensagens",
        "bot": "telegram_bot_config",
        "x": 150,
        "y": 100
    },
    {
        "id": "process_message",
        "type": "function",
        "name": "Processar Mensagem",
        "func": "// Processar mensagem do usuário\nmsg.payload = {\n    chatId: msg.payload.chatId,\n    message: msg.payload.content,\n    user: msg.payload.from\n};\nreturn msg;",
        "x": 350,
        "y": 100
    }
]
```

### 📡 Configuração do MQTT

#### Passo 1: Configurar Broker MQTT no Node-RED

1. No Node-RED, arraste um nó **mqtt in**
2. Duplo-clique para configurar
3. Clique no lápis ao lado de "Server"
4. Configure os parâmetros:
   - **Server**: `broker.hivemq.com` (ou seu broker)
   - **Port**: `1883`
   - **Client ID**: `nodered_client_${random}`
   - **Username/Password**: (se necessário)

#### Passo 2: Configurar Tópicos MQTT

```javascript
// Tópico padrão para dados climáticos
Topic: "ufg/2025/weather"

// Estrutura de dados esperada:
{
    "temperature": 28.5,
    "humidity": 65.2,
    "feels_like": 32.1,
    "pressure": 1013.25,
    "timestamp": "2025-09-22T10:30:00Z"
}
```

#### Passo 3: Nó de Processamento MQTT

```javascript
// Function node para processar dados MQTT
var data = JSON.parse(msg.payload);

msg.payload = {
    temperature: data.temperature,
    humidity: data.humidity,
    feels_like: data.feels_like,
    pressure: data.pressure,
    timestamp: new Date().toISOString()
};

return msg;
```

### 🗄️ Configuração do InfluxDB

#### Passo 1: Acessar Interface Web do InfluxDB

1. Abra: `http://localhost:8086`
2. Faça login com:
   - **Username**: `admin`
   - **Password**: `UFGInf2025@`

#### Passo 2: Configurar no Node-RED

1. Instale o nó InfluxDB:
   - **Menu** → **Manage Palette** → **Install**
   - Procure por `node-red-contrib-influxdb`
   - Clique em **Install**

2. Configure o nó InfluxDB:
   - Arraste um nó **influxdb out**
   - Configure a conexão:
     - **URL**: `http://influxdb:8086`
     - **Token**: `dafda90fasd8f0adsadacsda9s0djdad8a9sd`
     - **Organization**: `UFGInf2025`
     - **Bucket**: `UFG-Weather`

#### Passo 3: Estrutura de Dados no InfluxDB

```javascript
// Function node para formatar dados para InfluxDB
msg.payload = {
    measurement: "weather_data",
    fields: {
        temperature: parseFloat(msg.payload.temperature),
        humidity: parseFloat(msg.payload.humidity),
        feels_like: parseFloat(msg.payload.feels_like),
        pressure: parseFloat(msg.payload.pressure)
    },
    tags: {
        location: "goiania",
        sensor: "iot_sensor_01"
    },
    timestamp: new Date()
};

return msg;
```

### 🤖 Configuração do Google Gemini

#### Passo 1: Obter API Key

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Clique em **Create API Key**
3. Copie e salve a chave gerada

#### Passo 2: Instalar Nós HTTP no Node-RED

```javascript
// Function node para chamar Gemini API
var prompt = `Baseado nos dados climáticos atuais de Goiânia:
Temperatura: ${msg.weather.temperature}°C
Sensação térmica: ${msg.weather.feels_like}°C
Umidade: ${msg.weather.humidity}%

Pergunta do usuário: ${msg.user_message}

Recomende locais para visitar em Goiânia considerando o clima atual.`;

msg.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent";
msg.headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": "SUA_API_KEY_AQUI"
};
msg.payload = {
    contents: [{
        parts: [{
            text: prompt
        }]
    }]
};

return msg;
```

## 🔄 Fluxo Completo no Node-RED

### Importar Template

1. Copie o conteúdo do arquivo `template/Telegram.json`
2. No Node-RED: **Menu** → **Import** → **Clipboard**
3. Cole o JSON e clique em **Import**

### Configurar Fluxo Manualmente

Se preferir criar do zero, o fluxo deve seguir esta ordem:

```
[Telegram In] → [Processar Mensagem] → [Consultar InfluxDB] → [Chamar Gemini] → [Telegram Out]
     ↑                                         ↓
[MQTT In] → [Processar Dados] → [Salvar InfluxDB]
```

#### Código dos Function Nodes

**1. Processar Mensagem do Telegram:**
```javascript
if (msg.payload.content) {
    global.set("currentChatId", msg.payload.chatId);
    msg.user_message = msg.payload.content;
    return msg;
}
```

**2. Consultar Dados Recentes do InfluxDB:**
```javascript
// Query para buscar dados das últimas 2 horas
msg.query = `
from(bucket: "UFG-Weather")
  |> range(start: -2h)
  |> filter(fn: (r) => r["_measurement"] == "weather_data")
  |> filter(fn: (r) => r["location"] == "goiania")
  |> last()
`;

return msg;
```

**3. Preparar Resposta para Telegram:**
```javascript
var chatId = global.get("currentChatId");
var response = msg.payload.candidates[0].content.parts[0].text;

msg.payload = {
    chatId: chatId,
    type: "message",
    content: response
};

return msg;
```

## 🧪 Testando o Sistema

### 1. Verificar Serviços

```bash
# Verificar logs
docker-compose logs -f nodered
docker-compose logs -f influxdb

# Verificar conectividade
curl http://localhost:1880
curl http://localhost:8086/health
```

### 2. Testar MQTT

```bash
# Instalar cliente MQTT (opcional)
npm install -g mqtt

# Publicar dados de teste
mqtt pub -h broker.hivemq.com -t "ufg/2025/weather" -m '{"temperature":25.5,"humidity":68.2,"feels_like":27.8,"pressure":1015.3}'
```

### 3. Testar Bot do Telegram

1. Procure seu bot no Telegram pelo username
2. Digite `/start`
3. Envie uma mensagem: "Que locais recomendam para visitar hoje?"
4. Aguarde a resposta personalizada

## 📊 Monitoramento e Logs

### Visualizar Dados no InfluxDB

1. Acesse: `http://localhost:8086`
2. Vá em **Data Explorer**
3. Selecione:
   - **Bucket**: `UFG-Weather`
   - **Measurement**: `weather_data`
   - **Fields**: temperature, humidity, etc.

### Monitorar Node-RED

- **Debug**: Ative nós de debug nos fluxos
- **Logs**: `docker-compose logs -f nodered`
- **Dashboard**: Acesse `http://localhost:1880`

## 🔧 Solução de Problemas Comuns

### InfluxDB não conecta

```bash
# Verificar se o container está rodando
docker ps | grep influxdb

# Verificar logs
docker-compose logs influxdb

# Recriar container
docker-compose down influxdb
docker-compose up -d influxdb
```

### MQTT não recebe dados

1. Verificar configuração do broker
2. Confirmar tópico correto
3. Testar com cliente MQTT externo

### Telegram não responde

1. Verificar token do bot
2. Confirmar configuração no Node-RED
3. Verificar logs de erro

### Gemini API falha

1. Verificar quota da API
2. Confirmar chave válida
3. Verificar formato da requisição

## 📝 Próximos Passos

- [ ] Implementar mais sensores IoT
- [ ] Adicionar previsão do tempo
- [ ] Criar dashboard web
- [ ] Implementar notificações automáticas
- [ ] Adicionar mais locais turísticos

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Autores

- **Fernando** - *Desenvolvimento Inicial* - [Fernando-EngComputacao](https://github.com/Fernando-EngComputacao)

---

**💡 Dica para Estudantes**: Este projeto é uma excelente introdução aos conceitos de IoT, MQTT, bancos de série temporal e integração de APIs. Experimente modificar os fluxos e adicionar novas funcionalidades!