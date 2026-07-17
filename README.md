# Guia de Instalação e Execução do Projeto

Este repositório possui dois modos de execução válidos:

- Modo A: gRPC (serviço de relatórios)
- Modo B: MOM com RabbitMQ (auditoria e notificações por publish/subscribe)

Use apenas um modo por vez para evitar conflitos operacionais.

# Instalação das dependências
Antes de rodar pela primeira vez, instale as dependências em cada pasta.

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

# Serviço de Relatórios (gRPC) - somente Modo A
`cd servico_relatorios`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../requirements.txt`

# Websocket_notificacoes
`cd websocket_notificacoes`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r ../requirements.txt`

# Serviço de Auditoria - somente Modo B
`cd auditoria`

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

# Frontend
`cd frontend`

`npm install`

# Pré-requisitos do MOM (somente Modo B)
- Erlang/OTP 27.x 64 bits
- RabbitMQ Server 4.3.2
- Biblioteca Python `pika` (já incluída em `requirements.txt`)

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

Painel administrativo: http://127.0.0.1:15672

Usuário padrão: `guest`

Senha padrão: `guest`

Portas do RabbitMQ:
- 5672: AMQP
- 15672: painel administrativo

# Como rodar o projeto

Regra importante: os modos sao mutuamente exclusivos para operacao do fluxo principal.

- No Modo A (gRPC), nao iniciar o servico de auditoria.
- No Modo B (MOM), nao iniciar o servico de relatorios gRPC.

# Modo A — gRPC (Relatórios)
Abra 7 terminais e rode um comando em cada:

# Terminal 1 — Serviço de Médicos (porta 8001)
`cd servico_medicos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8001`

# Terminal 2 — Serviço de Agendamentos (porta 8002)
`cd servico_agendamentos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8002`

# Terminal 3 — Gateway (porta 8000)
`cd gateway`

`venv\Scripts\Activate.ps1`

`uvicorn main:app --reload --port 8000`

# Terminal 4 — Serviço de Relatórios gRPC (porta 8005)
Este serviço consulta Médicos e Agendamentos. Inicie depois dos terminais 1 e 2.

`cd servico_relatorios`

`venv\Scripts\Activate.ps1`

`python server.py`

# Terminal 5 — Serviço SOAP (porta 8003)
`cd soap_convenios/servidor`

`venv\Scripts\Activate.ps1`

`python servidor.py`

# Terminal 6 — Frontend (porta 3000)
`cd frontend`

`npm start`

# Terminal 7 — Serviço de Notificações WebSocket (porta 8004)
`cd websocket_notificacoes`

`venv\Scripts\Activate.ps1`

`uvicorn server:app --reload --port 8004`

# Modo B — MOM (RabbitMQ + Auditoria)
Abra 8 terminais e rode um comando em cada:

# Terminal 1 — RabbitMQ (confirmação de status)
`Get-Service RabbitMQ`

# Terminal 2 — Serviço de Médicos (porta 8001)
`cd servico_medicos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8001`

# Terminal 3 — Serviço de Agendamentos (porta 8002)
Este serviço publica o evento `novo_agendamento` na exchange `agendamentos`.

`cd servico_agendamentos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8002`

# Terminal 4 — Gateway (porta 8000)
`cd gateway`

`venv\Scripts\Activate.ps1`

`uvicorn main:app --reload --port 8000`

# Terminal 5 — Serviço de Notificações WebSocket (porta 8004)
Este serviço consome a fila `fila_websocket`.

`cd websocket_notificacoes`

`venv\Scripts\Activate.ps1`

`uvicorn server:app --reload --port 8004`

# Terminal 6 — Serviço de Auditoria
Este serviço consome a fila `fila_auditoria`.

`cd auditoria`

`venv\Scripts\Activate.ps1`

`python main.py`

# Terminal 7 — Serviço SOAP (porta 8003)
`cd soap_convenios/servidor`

`venv\Scripts\Activate.ps1`

`python servidor.py`

# Terminal 8 — Frontend (porta 3000)
`cd frontend`

`npm start`

# Arquitetura MOM
- Abordagem: Publish/Subscribe
- Broker: RabbitMQ
- Exchange: `agendamentos`
- Tipo: `fanout`
- Publicador: `servico_agendamentos`
- Assinante 1: `websocket_notificacoes` (fila `fila_websocket`)
- Assinante 2: `auditoria` (fila `fila_auditoria`)
- Evento: `novo_agendamento`

# Checklist de validação pós-pull

# Modo A — gRPC
1. Subir os 7 serviços do Modo A.
2. Confirmar que o servico de auditoria NAO esta em execucao.
3. Abrir `http://localhost:8000/relatorios/dashboard` e confirmar resposta JSON.
4. Abrir o frontend e validar carregamento da aba de relatórios.

# Modo B — MOM
1. Confirmar RabbitMQ ativo com `Get-Service RabbitMQ`.
2. Subir os 8 serviços do Modo B.
3. Confirmar que o servico de relatorios gRPC NAO esta em execucao.
4. Criar um novo agendamento no frontend.
5. Confirmar logs:
	- Agendamentos: `[MOM] Evento publicado no RabbitMQ`
	- WebSocket: `[MOM] Evento recebido`
	- Auditoria: `[AUDITORIA] Evento recebido`

# Como rodar o cliente Java
Com o servidor SOAP rodando, execute em um terminal separado:

`cd soap_convenios/cliente`

`java ClienteSOAP`

# Links úteis

# Comuns aos dois modos
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

# Somente Modo A — gRPC
| O que é | URL |
| --- | --- |
| Serviço gRPC de Relatórios | localhost:8005 |
| Dashboard de Relatórios via Gateway | http://localhost:8000/relatorios/dashboard |

# Somente Modo B — MOM
| O que é | URL |
| --- | --- |
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
| 8005 | Serviço gRPC de Relatórios (Modo A) |
| 5672 | RabbitMQ AMQP (Modo B) |
| 15672 | Painel RabbitMQ (Modo B) |
