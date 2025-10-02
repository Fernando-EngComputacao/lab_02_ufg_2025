# Assistente Telegram com IA para Recomendações Climáticas - Parte B

## 🌟 Sobre o Projeto

Esta parte do projeto implementa um assistente inteligente no Telegram que fornece recomendações personalizadas de locais para visitar em Goiânia, baseando-se em dados climáticos históricos armazenados no InfluxDB. Utiliza IA (Google Gemini) para processar consultas e gerar respostas contextualizadas.

### 📋 Funcionalidades Principais

- 🤖 **Assistente Telegram**: Bot interativo para receber consultas dos usuários
- 🧠 **IA Integrada**: Processamento com Google Gemini para respostas contextualizadas
- 📊 **Consulta a Dados Históricos**: Recuperação de dados climáticos do InfluxDB
- 🔄 **Node-RED**: Orquestração de fluxos e integrações

### 🏗️ Arquitetura do Sistema

```
[Telegram Bot] → [Node-RED] → [InfluxDB] → [Gemini AI] → [Resposta ao Usuário]
```

## 📋 Pré-requisitos

### Software Necessário

- [Docker](https://docs.docker.com/get-docker/) (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0+)
- Git

### Contas e APIs Necessárias

- **Telegram Bot Token**: Criar bot via @BotFather
- **Google Gemini API Key**: Conta no Google Cloud Platform

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

Copie o arquivo `.env` e configure as variáveis relacionadas ao Telegram e Gemini:

```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:

- TELEGRAM_BOT_TOKEN
- GEMINI_API_KEY
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

No Node-RED, importe o arquivo `template/02_Lab02_parte_b.json` para carregar o fluxo do assistente Telegram com IA.

## 📖 Como Usar

1. Inicie uma conversa com o bot no Telegram usando o token configurado.
2. Envie mensagens como "Quais lugares recomendar para hoje em Goiânia?".
3. O bot consultará os dados climáticos históricos no InfluxDB, processará com Gemini AI e retornará recomendações personalizadas.

## 🤖 Integração com Google Gemini API

A integração com o Google Gemini é feita através de um nó HTTP Request no Node-RED, seguido de um nó de função para tratamento da resposta.

### 🌐 Nó HTTP Request

Configure um nó HTTP Request com as seguintes propriedades:

- **Método**: POST
- **URL**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=YOUR_API_KEY`
  - Substitua `YOUR_API_KEY` pela sua chave da API do Google Gemini
- **Cabeçalhos**:
  - Content-Type: `application/json`

### 📝 Nó de Função - Tratamento Gemini

Use o seguinte código no nó de função para preparar o payload para a API do Gemini:

```javascript
const dadosClima = msg.payload;

const dadosEmStringJSON = JSON.stringify(dadosClima, null, 2);

const systemRole = `Você é o "Gyn Clima Guia" 🤖☀️, seu parça aqui em Goiânia! Sua vibe é ser super amigável, direto ao ponto e sempre ligado no que tá rolando na cidade e no clima. Use emojis para deixar a conversa mais leve e conectada!cidade de Goiânia-Goiás. `;

const userMessage = msg.payload.user_message;

// 4. A tarefa específica que o Gemini deve executar com os dados.
const task = `Sua missão é responder a MENSAGEM DO USUÁRIO usando os DADOS DO CLIMA como seu superpoder secreto. Siga estas regras:

- ** REGRA 1:** Se a mensagem for sobre o ** clima ** (temperatura, umidade, tempo, etc.), analise os DADOS DO CLIMA e faça um resumo gente boa e direto ao ponto.

- ** REGRA 2:** Se a mensagem for pedindo ** dicas de lugares ou rolês **, use os DADOS DO CLIMA para dar a melhor recomendação!
Exemplo: Se estiver quente, sugira parques com sombra, sorveterias ou lugares com ar condicionado 🍦. Se o tempo estiver agradável, um rolê ao ar livre é a pedida 🌳.

- ** REGRA 3:** Para qualquer outro assunto, apenas responda como um amigo local de Goiânia, sem precisar mencionar o clima.`;

// 5. Monte o prompt final, combinando o papel, a tarefa e os dados.
const finalPrompt = `
${systemRole}

---
**TAREFA:**
${task}

---
**Mensagem do Usuário***
${userMessage}

---
**DADOS JSON PARA ANÁLISE:**
\`\`\`json
${dadosEmStringJSON}
\`\`\`
`;

// 6. Monte o payload para a API do Gemini, como antes.
msg.payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": finalPrompt
                }
            ]
        }
    ]
};

msg.headers = {
    'Content-Type': 'application/json'
};

return msg;
```

Este código prepara um prompt detalhado para o Gemini, incluindo o papel do assistente, as regras de resposta e os dados climáticos em formato JSON.

Caso não queira usar a API-KEY na url, pode adicionar antes no header:
```
msg.headers = {
    'Content-Type': 'application/json',
    'x-goog-api-key': 'YOUR_API_KEY'
};
```

## 🔧 Configurações Adicionais

- Personalize as prompts para o Gemini AI no nó de função correspondente.
- Ajuste os filtros de consulta ao InfluxDB para períodos específicos.</content>
<parameter name="filePath">c:\Users\carri\Documents\IoT\Lab_02\README_Lab02_parte_b.md