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

**Docker compose**

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m)" -o /usr/libexec/docker/cli-plugins/docker-compose
sudo chmod +x /usr/libexec/docker/cli-plugins/docker-compose
docker compose version
```

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/Fernando-EngComputacao/lab_02_ufg_2025.git
cd lab_02_ufg_2025
```

### 2. Iniciar os Serviços

```bash
docker-compose up -d
```

### 3. Acessar Node-RED

Abra o navegador em `http://<seu_endereco_ipv4>:1880` (o IP do seu servidor da sua instância EC2).

### 4. Importar o Fluxo

No Node-RED, importe o arquivo `template/01_Lab02_parte_a.json` para carregar o fluxo de captura de dados via MQTT.

## 📖 Como Usar

1. Configure os sensores IoT para publicar dados no tópico MQTT `ufg/2025/cmu/weather`.
2. Os dados serão capturados pelo Node-RED e armazenados no InfluxDB.
3. Monitore os dados através do painel de debug no Node-RED ou consultas diretas ao InfluxDB.

## 🐍 Publicador Python para MQTT

Para instruções detalhadas sobre como configurar um script Python para publicar dados climáticos no MQTT, consulte o documento [Publicador Python para MQTT](README_Python_Publisher.md).

# Node-RED  

## 📋 Pacotes Node-RED Necessários

Para o funcionamento completo do sistema, instale os seguintes pacotes no Node-RED:

Na tela do Node-RED, localize o menu sanduíche (canto superior direito). Ao selecionar, vá até a opção 'Gerenciar Paletas'. 
Na aba 'Instalar' coloque o nome dos pacotes abaixo um por vez e os instalem.

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

Observação: instale um pacote por vez e aguarde cada pacote a instalar para evitar conflitos e erros.


## 🔍 Acesso ao InfluxDB

O InfluxDB está configurado no Docker Compose e pode ser acessado através do navegador ou ferramentas de linha de comando.

### 🌐 Acesso via Navegador

1. **URL de Acesso**: `http://<SEU_IP_PUBLICO_EC2>:8086`
   - Substitua `<SEU_IP_PUBLICO_EC2>` pelo endereço IPv4 público da sua instância EC2.

2. **Credenciais de Login**:
   - **Usuário**: `admin`
   - **Senha**: `UFGInf2025@`
   - **Organização**: `UFGInf2025`
   - **Bucket**: `UFG-Weather`
   - **Token**: `dafda90fasd8f0adsadacsda9s0djdad8a9sd`

3. **Como Acessar**:
   - Abra o navegador e navegue até a URL acima.
   - Faça login com as credenciais fornecidas.
   - Você poderá visualizar dashboards, consultar dados e gerenciar buckets.


## 📝 Função de Tratamento InfluxDB

Use o seguinte código no nó de função para preparar os dados para o InfluxDB:

```javascript
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

---


## 🔧 Configurações Adicionais

- Ajuste os tópicos MQTT conforme necessário.
- Configure retenção de dados no InfluxDB para otimizar armazenamento.