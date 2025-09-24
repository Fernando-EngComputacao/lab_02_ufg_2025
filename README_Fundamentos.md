# 📚 Fundamentos e Tecnologias Utilizadas

Este documento fornece uma visão geral das tecnologias e conceitos fundamentais utilizados no projeto. Ele é recomendado para quem deseja entender melhor os componentes e suas funções.

---

## 🔄 Node-RED

🛠️ **Node-RED** é uma ferramenta de programação visual para conectar dispositivos, APIs e serviços de maneira simples. Ele é amplamente utilizado em projetos de IoT para orquestrar fluxos de dados.

- 🌐 **Site oficial**: [https://nodered.org/](https://nodered.org/)
- 📖 **Documentação**: [https://nodered.org/docs/](https://nodered.org/docs/)

---

## 📊 InfluxDB

🕒 **InfluxDB** é um banco de dados de série temporal otimizado para armazenar e consultar grandes volumes de dados que variam com o tempo, como leituras de sensores.

- 🌐 **Site oficial**: [https://www.influxdata.com/](https://www.influxdata.com/)
- 📖 **Documentação**: [https://docs.influxdata.com/](https://docs.influxdata.com/)

### ⏱️ O que é um Banco de Dados de Série Temporal?

Um banco de dados de série temporal é projetado para lidar com dados que possuem um carimbo de tempo associado. Exemplos incluem medições de sensores, logs de eventos e dados financeiros.

**Vantagens**:
- ⚡ Otimizado para consultas baseadas em tempo.
- 📦 Compactação eficiente de dados históricos.

---

## 📡 MQTT

📨 **MQTT** (Message Queuing Telemetry Transport) é um protocolo leve de comunicação projetado para dispositivos IoT. Ele utiliza um modelo de publicação/assinatura para troca de mensagens.

- 🌐 **Site oficial**: [https://mqtt.org/](https://mqtt.org/)
- 📖 **Documentação**: [https://mqtt.org/documentation](https://mqtt.org/documentation)

### 🔄 Como Funciona?

1. 🏠 **Broker**: O servidor central que gerencia as mensagens.
2. 📤 **Publisher**: Dispositivo que envia mensagens para um tópico.
3. 📥 **Subscriber**: Dispositivo que recebe mensagens de um tópico.

---

## 🤖 Google Gemini API

🧠 **Google Gemini** é uma API de inteligência artificial que permite criar modelos avançados para processamento de linguagem natural e outras tarefas.

### 🔑 Como Obter o Token de API?

1. 🌐 Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. ➕ Crie um novo projeto ou selecione um existente.
3. ✅ Ative a API do Google Gemini.
4. 🔐 Vá para "Credenciais" e clique em "Criar Credenciais".
5. 🔑 Escolha "Chave de API" e copie o token gerado.

---

## 🛠️ Outros Conceitos Importantes

### 🐳 Docker

🐳 **Docker** é uma plataforma de containerização open-source que permite empacotar aplicações e suas dependências em contêineres leves e portáteis. Isso facilita a implantação, execução e escalabilidade consistente de aplicações em diferentes ambientes, desde desenvolvimento local até produção em nuvem.

#### � Como Funciona?

- **Contêineres**: Unidades leves e isoladas que executam aplicações, compartilhando o kernel do sistema operacional host, o que os torna eficientes.
- **Imagens**: Modelos imutáveis e leves que contêm tudo necessário para executar uma aplicação (código, bibliotecas, dependências).
- **Docker Engine**: O runtime que constrói, executa e gerencia contêineres.
- **Dockerfile**: Arquivo de configuração usado para criar imagens personalizadas.

**Vantagens**:
- 🚀 Portabilidade: Execute em qualquer lugar com Docker instalado.
- ⚡ Eficiência: Contêineres são mais leves que máquinas virtuais.
- 🔒 Isolamento: Aplicações não interferem umas nas outras.

- 🌐 **Site oficial**: [https://www.docker.com/](https://www.docker.com/)
- 📖 **Documentação oficial**: [https://docs.docker.com/](https://docs.docker.com/)

### 📋 Docker Compose

📋 **Docker Compose** é uma ferramenta para definir e gerenciar aplicações multi-contêiner usando arquivos YAML. Permite orquestrar vários serviços relacionados em um único comando.

### 📱 Telegram Bot

- 🤖 **BotFather**: Ferramenta oficial do Telegram para criar e gerenciar bots.
- 📖 **Documentação**: [https://core.telegram.org/bots](https://core.telegram.org/bots)

---

💡 **Este documento será atualizado conforme necessário para incluir mais informações e recursos úteis.**