# Frontend — Sistema de Agendamento de Consultas

Interface React que consome os dois serviços do sistema distribuído.

---

## Como rodar

```bash
cd frontend
npm start
```

> Os backends precisam estar rodando antes de abrir o frontend.

---

## Backends necessários

| Serviço | Porta | Como rodar |
|---|---|---|
| servico_medicos | 8001 | `python manage.py runserver 8001` |
| servico_agendamentos | 8002 | `python manage.py runserver 8002` |

---

## Comunicação com os backends (Proxy)

### O problema

O frontend React roda em `localhost:3000`. Os backends Django rodam em `localhost:8001` e `localhost:8002`. Quando o browser tenta fazer uma requisição de uma porta para outra, ele bloqueia por segurança — isso se chama **política de mesma origem (CORS)**.

No Codespaces o problema é ainda pior: cada porta tem uma URL diferente, e o browser bloqueia requisições entre URLs distintas.

### A solução: Proxy

O arquivo `src/setupProxy.js` configura o próprio servidor do React como **intermediário**:

```
Browser → React (porta 3000) → Django Médicos (porta 8001)
Browser → React (porta 3000) → Django Agendamentos (porta 8002)
```

O browser faz tudo para a porta 3000 (mesma origem, sem bloqueio). O React dev server recebe e **repassa** para o backend correto nos bastidores.

### As regras do proxy

```js
// /medicos e /especialidades → vai para porta 8001
app.use(['/medicos', '/especialidades'], proxy({ target: 'http://localhost:8001' }))

// /agendas e /agendamentos → vai para porta 8002
app.use(['/agendas', '/agendamentos'], proxy({ target: 'http://localhost:8002' }))
```

### O que isso muda no código

As URLs das requisições são **relativas** (sem host):

```js
fetch('/medicos/')       // o proxy encaminha para http://localhost:8001/medicos/
fetch('/agendamentos/')  // o proxy encaminha para http://localhost:8002/agendamentos/
```

| Arquivo | O que faz |
|---|---|
| `src/setupProxy.js` | Define as regras de redirecionamento |
| `src/api.js` | Usa URLs relativas, deixando o proxy resolver o destino |
