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

### 1. Acessar Node-RED

Abra o navegador em `http://<seu_endereco_ipv4>:1880` (o IP do seu servidor da sua instância EC2).

### 2. Importar o Fluxo

No Node-RED, importe o arquivo `template/02_Lab02_parte_b.json` para carregar o fluxo do assistente Telegram com IA.

## 📖 Como Usar

1. Inicie uma conversa com o bot no Telegram usando o token configurado.
2. Envie mensagens como "Quais lugares recomendar para hoje em Goiânia?".
3. O bot consultará os dados climáticos históricos no InfluxDB, processará com Gemini AI e retornará recomendações personalizadas.

## 🤖 Integração com Google Gemini API

A integração com o Google Gemini é feita através de um nó HTTP Request no Node-RED, seguido de um nó de função para tratamento da resposta.

### 🔑 Como Obter a API Key do Google Gemini

Para usar a API do Google Gemini, você precisa de uma chave de API. Siga os passos abaixo:

1. Acesse o [Google AI Studio](https://aistudio.google.com/app/api-keys).
2. Faça login com sua conta Google (se necessário).
3. Clique em "Create API Key" ou "Criar chave de API".
4. Copie a chave gerada e guarde em local seguro.
5. Use essa chave na URL do nó HTTP Request, substituindo `YOUR_API_KEY`.

**Nota**: Mantenha sua chave de API segura e não a compartilhe publicamente.

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
- Ajuste os filtros de consulta ao InfluxDB para períodos específicos.


## 📱 Configuração do Telegram Bot

Para integrar o assistente com o Telegram, você precisa criar um bot e obter as credenciais necessárias.

### 🤖 Como Criar um Bot no Telegram

1. Abra o Telegram e procure por **@BotFather**.
2. Inicie uma conversa com o BotFather clicando em "Start".
3. Envie o comando `/newbot`.
4. Siga as instruções:
   - Digite um nome para o seu bot (ex: "Gyn Clima Guia").
   - Digite um username único para o bot (deve terminar com "bot", ex: "gyn_clima_bot").
5. O BotFather fornecerá o **token de acesso** do bot. Guarde esse token em local seguro.

### 🔑 Como Obter o Token e ID do Bot

- **Token**: É fornecido diretamente pelo BotFather após criar o bot. Exemplo: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
- **ID do Bot**: O ID é a parte antes dos dois pontos no token. No exemplo acima, seria `123456`.

### 💬 Como Obter o ID do Seu Chat no Telegram

Para que o bot possa enviar mensagens para você, precisa do ID do chat:

1. **Parte 01 - Via Bot**:
   - Inicie uma conversa com seu bot recém-criado.
   - Envie qualquer mensagem para o bot.
   - Acesse: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
     - Substitua `<SEU_TOKEN>` pelo token do seu bot.

2. **Parte 02 - Via Bot de Terceiros**:
   - Use o bot @UserInfeBot.
   - Envie `/start` para ele.
   - Ele responderá com seu ID de usuário, que pode ser usado como ID do chat para mensagens privadas.

3. **Parte 03 - Via @UserInfeBot**:
   - Procure pelo bot @UserInfeBot no Telegram.
   - Inicie uma conversa enviando qualquer mensagem.
   - O bot responderá automaticamente com seu ID de usuário.
   - Use esse ID como ID do chat para mensagens privadas.


## 📤 Nó Telegram Sender

Após processar a resposta do Gemini, use um nó Telegram Sender para enviar a mensagem formatada para o chat.

### 📝 Formatação do Corpo da Mensagem

Use o seguinte código no nó de função antes do nó Telegram Sender para formatar o payload:

```javascript
const textoDaResposta = msg.payload.candidates[0].content.parts[0].text;

msg.payload = {
    "type": "message",
    "chatId": seu_chat_id,
    "content": "Alex: " + textoDaResposta
};

return msg;
```

**Explicação**:
- `textoDaResposta`: Extrai o texto da resposta do Gemini.
- `type`: Define o tipo como "message".
- `chatId`: Substitua `seu_chat_id` pelo ID do seu chat Telegram (obtido conforme explicado anteriormente).
- `content`: Formata a mensagem com o prefixo "Alex: " seguido da resposta do Gemini.

Configure o nó Telegram Sender com o token do bot e conecte-o após este nó de função.

**Nota**: Use o ID do chat nas configurações do Node-RED para enviar mensagens para o seu Telegram.

## 📊 Query do InfluxDB

Para consultar os dados climáticos armazenados no InfluxDB, use a seguinte query Flux no nó InfluxDB:

```flux
from(bucket: "UFG-Weather")
  |> range(start: -1h) // Busca no histórico da última hora
  |> filter(fn: (r) => r._measurement == "UFG-2025")
  |> filter(fn: (r) => r.location == "Goiania GO")
  |> filter(fn: (r) => r._field == "temperatura" or r._field == "umidade" or r._field == "sensacao_termica")
```

**Explicação da Query**:
- `from(bucket: "UFG-Weather")`: Seleciona o bucket onde os dados estão armazenados.
- `range(start: -1h)`: Filtra dados da última hora (pode ajustar para outros períodos, ex: `-24h` para último dia).
- `filter(fn: (r) => r._measurement == "UFG-2025")`: Filtra pela medição específica.
- `filter(fn: (r) => r.location == "Goiania GO")`: Filtra pela localização.
- `filter(fn: (r) => r._field == "temperatura" or r._field == "umidade" or r._field == "sensacao_termica")`: Seleciona apenas os campos de interesse.

## 🔄 Formatação dos Dados para Gemini

Após consultar o InfluxDB, use o seguinte código no nó de função para formatar os dados brutos em um objeto estruturado para enviar ao Gemini:

- Nó (Dados InfluxDB)

```javascript
// 1. Inicializa o objeto final já com as chaves e arrays vazios.
const resultado = {
    temperatura: [],
    umidade: [],
    sensacao_termica: [],
    user_message: String
};

// 2. Pega o array de dados brutos que veio do InfluxDB.
const dadosBrutos = msg.payload;

// 3. Itera sobre cada registro (cada ponto de dado) que o InfluxDB retornou.
for (const registro of dadosBrutos) {
    // Pega o nome do campo (ex: "temperatura")
    const campo = registro._field;
    // Pega o valor (ex: 33.38)
    const valor = registro._value;

    // 4. Adiciona o valor ao array correspondente dentro do objeto 'resultado'.
    // Verifica se a chave existe para evitar erros.
    if (resultado[campo]) {
        resultado[campo].push(valor);
    }
}
resultado.user_message = flow.get('user_message');

msg.payload = resultado;
return msg;
```

**Explicação do Código**:
- Inicializa um objeto `resultado` com arrays vazios para cada campo climático e uma string para a mensagem do usuário.
- Itera sobre os dados brutos do InfluxDB, extraindo o campo (`_field`) e valor (`_value`) de cada registro.
- Adiciona os valores aos arrays correspondentes no objeto `resultado`.
- Recupera a mensagem do usuário armazenada no contexto do flow.
- Define `msg.payload` como o objeto formatado para ser enviado ao Gemini.