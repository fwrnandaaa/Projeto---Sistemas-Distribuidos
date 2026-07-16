# Guia de Instalação e Execução do Projeto

# Instalação das dependências
Antes de rodar pela primeira vez, instale as dependências em cada pasta.

# Pré-requisitos do MOM
- Erlang/OTP 27.x 64 bits
- RabbitMQ Server 4.3.2
- Biblioteca Python `pika`

# Configuração inicial do RabbitMQ no Windows
Abra o PowerShell como administrador.

Entre na pasta do RabbitMQ:

`cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin"`

Habilite o painel administrativo:

`.\rabbitmq-plugins.bat enable rabbitmq_management`

Verifique o RabbitMQ:

`.\rabbitmqctl.bat status`

Inicie o serviço, se necessário:

`Start-Service RabbitMQ`

Verifique o serviço:

`Get-Service RabbitMQ`

O painel administrativo está disponível em http://127.0.0.1:15672.

Usuário: `guest`

Senha: `guest`

Portas utilizadas pelo RabbitMQ:
- 5672: comunicação AMQP usada pelas aplicações
- 15672: painel administrativo

# Serviço de Médicos
`cd servico_medicos` 

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../requirements.txt`

# Serviço de Agendamentos

`cd servico_agendamentos`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../requirements.txt`

# Gateway
`cd gateway`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../requirements.txt`

# Serviço SOAP (Convênios)
`cd soap_convenios/servidor`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../../requirements.txt`

# Cliente Java (Convênios)
`cd soap_convenios/cliente`

`javac ClienteSOAP.java`

# Websocket_notificacoes 
`cd websocket_notificacoes`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../requirements.txt`

# Serviço de Auditoria

`cd auditoria`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../requirements.txt`

# Frontend
`cd frontend`

`npm install`

# Como rodar o projeto
Abra 7 terminais e rode um comando em cada:

# Terminal 1 — Serviço de Médicos (porta 8001)
`cd servico_medicos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8001`

# Terminal 2 — Serviço de Agendamentos (porta 8002)
Este serviço publica o evento `novo_agendamento` na exchange `agendamentos`.

`cd servico_agendamentos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8002`

# Terminal 3 — Gateway (porta 8000)
`cd gateway`

`venv\Scripts\Activate.ps1`

`uvicorn main:app --reload --port 8000`

# Terminal 4 — Serviço SOAP (porta 8003)
`cd soap_convenios/servidor`

`venv\Scripts\Activate.ps1`

`python servidor.py`

# Terminal 5 — Frontend (porta 3000)
`cd frontend`

`npm start`

# Terminal 6 — Serviço de Notificações WebSocket (porta 8004)

Este serviço é um assinante do RabbitMQ, consome a fila `fila_websocket` e encaminha o evento ao frontend via WebSocket.

`cd websocket_notificacoes`

`venv\Scripts\Activate.ps1`

`uvicorn server:app --reload --port 8004`

# Terminal 7 — Serviço de Auditoria

Este serviço é o segundo assinante e consome a fila `fila_auditoria`.

`cd auditoria`

`venv\Scripts\Activate.ps1`

`python main.py`

# Arquitetura MOM

- Abordagem: Publish/Subscribe
- Broker: RabbitMQ
- Exchange: `agendamentos`
- Tipo: `fanout`
- Publicador: `servico_agendamentos`
- Assinante 1: `websocket_notificacoes`
- Fila: `fila_websocket`
- Assinante 2: `auditoria`
- Fila: `fila_auditoria`
- Evento: `novo_agendamento`

# Como testar o MOM

1. Confirmar que o RabbitMQ está em execução.
2. Iniciar o serviço WebSocket.
3. Iniciar a auditoria.
4. Iniciar os demais serviços.
5. Abrir o frontend.
6. Criar um novo agendamento.
7. Confirmar os logs:
   - Serviço de agendamentos: `[MOM] Evento publicado no RabbitMQ`
   - WebSocket: `[MOM] Evento recebido`
   - Auditoria: `[AUDITORIA] Evento recebido`

# Como verificar no RabbitMQ

- Acesse http://127.0.0.1:15672.
- Abra “Queues and Streams”.
- Confirme as filas:
  - `fila_websocket`
  - `fila_auditoria`
- Abra “Exchanges”.
- Confirme a exchange:
  - `agendamentos`

# Como rodar o cliente Java
Com o servidor SOAP rodando, execute em um terminal separado:

`cd soap_convenios/cliente`

`java ClienteSOAP`

# Links úteis
| O que é | URL |
| --- | --- |
| Frontend | http://localhost:3000 |
| Gateway | http://localhost:8000 |
| Swagger (documentação) | http://localhost:8000/docs |
| API Médicos | http://localhost:8001/medicos/ |
| API Agendamentos | http://localhost:8002/agendamentos/ |
| Admin Médicos | http://localhost:8001/admin |
| Admin Agendamentos | http://localhost:8002/admin |
| Servidor SOAP | http://localhost:8003 |
| WSDL | http://localhost:8003/?wsdl |
| Serviço de Notificações WebSocket | ws://localhost:8004/ws/notificacoes |
| Health Check do WebSocket | http://localhost:8004/health |
| Painel RabbitMQ | http://127.0.0.1:15672 |

# Portas dos serviços

| Porta | Serviço |
| --- | --- |
| 3000 | Frontend |
| 8000 | Gateway |
| 8001 | Serviço de Médicos |
| 8002 | Serviço de Agendamentos |
| 8003 | Serviço SOAP |
| 8004 | WebSocket |
| 5672 | RabbitMQ AMQP |
| 15672 | Painel RabbitMQ |
