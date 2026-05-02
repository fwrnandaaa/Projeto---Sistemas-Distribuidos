# Guia de Instalação e Execução do Projeto

# Instalação das dependências
Antes de rodar pela primeira vez, instale as dependências em cada pasta.

# Serviço de Médicos
`cd servico_medicos` 

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r requirements.txt`

# Serviço de Agendamentos

`cd servico_agendamentos`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r requirements.txt`

# Gateway
`cd gateway_fastapi`

`python -m venv venv`

`venv\Scripts\Activate.ps1`

`pip install -r requirements.txt`

# Frontend
`cd frontend`

`npm install`

# Como rodar o projeto
Abra 4 terminais e rode um comando em cada:

# Terminal 1 — Serviço de Médicos (porta 8001)
`cd servico_medicos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8001`

# Terminal 2 — Serviço de Agendamentos (porta 8002)
`cd servico_agendamentos`

`venv\Scripts\Activate.ps1`

`python manage.py runserver 0.0.0.0:8002`

# Terminal 3 — Gateway (porta 8000)
`cd gateway_fastapi`

`venv\Scripts\Activate.ps1`

`uvicorn main:app --reload --port 8000`

# Terminal 4 — Frontend (porta 3000)
`cd frontend`
`npm start`

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