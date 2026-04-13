# Guia de Configuração do Projeto
O QUE RODAR ANTES DE COMEÇAR A PROGRAMAR
(O de médico eu já fiz)
## Serviço de Médicos (porta 8001)

### 1. Entrar na pasta e ativar o venv
```bash
cd servico_medicos
source venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install django djangorestframework django-cors-headers
```

### 3. Rodar o serviço
```bash
python manage.py runserver 8001
```

---

## Serviço de Agendamentos (porta 8002)

### 1. Entrar na pasta e ativar o venv
```bash
cd servico_agendamentos
source venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install django djangorestframework django-cors-headers
```

### 3. Rodar o serviço
```bash
python manage.py runserver 8002
```

---

## Gateway (porta 8000)

### 1. Entrar na pasta e ativar o venv
```bash
cd gateway
source venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install django djangorestframework requests drf-yasg django-cors-headers
```

### 3. Rodar o gateway
```bash
python manage.py runserver 8000
```

---

## Ordem para rodar o projeto completo

Abra **3 terminais separados** e rode um em cada:

| Terminal | Comando |
|---|---|
| Terminal 1 | `cd servico_medicos && source venv/bin/activate && python manage.py runserver 8001` |
| Terminal 2 | `cd servico_agendamentos && source venv/bin/activate && python manage.py runserver 8002` |
| Terminal 3 | `cd gateway && source venv/bin/activate && python manage.py runserver 8000` |

---

## Links úteis quando estiver rodando

| O que é | URL |
|---|---|
| API de médicos | http://localhost:8001/medicos/ |
| API de agendamentos | http://localhost:8002/consultas/ |
| Gateway | http://localhost:8000/api/ |
| Swagger (documentação) | http://localhost:8000/swagger/ |

---

## Observações importantes

- Sempre ative o `venv` antes de instalar qualquer coisa
- Os 3 serviços precisam estar rodando ao mesmo tempo
- O gateway depende dos outros dois — rode os serviços antes do gateway