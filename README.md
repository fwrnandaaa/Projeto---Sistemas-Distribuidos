# Guia de Instalação e Execução do Projeto

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

# Frontend
`cd frontend`

`npm install`

# Como rodar o projeto
Abra 6 terminais e rode um comando em cada:

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

# Terminal 4 — Serviço SOAP (porta 8003)
`cd soap_convenios/servidor`

`venv\Scripts\Activate.ps1`

`python servidor.py`

# Terminal 5 — Frontend (porta 3000)
`cd frontend`

`npm start`

# Terminal 6 — Serviço de Notificações WebSocket (porta 8004)

`cd websocket_notificacoes`

`venv\Scripts\Activate.ps1`

`uvicorn server:app --reload --port 8004`

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