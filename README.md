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
                 [Telegram Bot] ← [Gemini AI] 
```


## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Autores

- **Fernando** - *Desenvolvimento Inicial* - [Fernando-EngComputacao](https://github.com/Fernando-EngComputacao)
  - Email: furtado.fernando@discente.ufg.br
  - LinkedIn: https://www.linkedin.com/in/furtadof/

- Sobre o **Fernando**: [Lattes](http://lattes.cnpq.br/0222161974009571) - [Instagram](https://www.instagram.com/_fernando_furtado_/)


---

**💡 Dica para Estudantes**: Este projeto é uma excelente introdução aos conceitos de IoT, MQTT, bancos de série temporal e integração de APIs. Experimente modificar os fluxos e adicionar novas funcionalidades!