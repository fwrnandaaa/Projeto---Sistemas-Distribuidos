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

Em Codespaces, o problema é ainda maior: cada porta tem uma URL diferente, e o browser bloqueia requisições entre URLs distintas.

### A solução: Proxy com caminhos relativos

O arquivo `src/setupProxy.js` configura o próprio servidor do React como **intermediário**, e o `src/api.js` usa **caminhos relativos** para as requisições:

```
Browser → React (porta 3000) → Django Médicos (porta 8001)
Browser → React (porta 3000) → Django Agendamentos (porta 8002)
```

O browser faz tudo para a porta 3000 (mesma origem, sem bloqueio). O React dev server recebe e **repassa** para o backend correto nos bastidores.

### Como funciona: setupProxy.js

O arquivo `src/setupProxy.js` define as regras de redirecionamento:

```js
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  // Requisições para /medicos e /especialidades → porta 8001
  app.use(
    ['/medicos', '/especialidades'],
    createProxyMiddleware({ target: 'http://localhost:8001', changeOrigin: true })
  );
  
  // Requisições para /agendas e /agendamentos → porta 8002
  app.use(
    ['/agendas', '/agendamentos'],
    createProxyMiddleware({ target: 'http://localhost:8002', changeOrigin: true })
  );
};
```

### Como funciona: Caminhos relativos em api.js

No arquivo `src/api.js`, **todas as URLs são relativas** (sem `http://localhost:PORT`):

```js
export const api = {
  // Caminhos relativos — o proxy encaminha para http://localhost:8001
  getMedicos: () => fetch('/medicos/').then(r => r.json()),
  getEspecialidades: () => fetch('/especialidades/').then(r => r.json()),
  
  // Caminhos relativos — o proxy encaminha para http://localhost:8002
  getAgendas: () => fetch('/agendas/').then(r => r.json()),
  createAgenda: (data) =>
    fetch('/agendas/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()),
  
  getAgendamentos: () => fetch('/agendamentos/').then(r => r.json()),
  // ... etc
};
```

### O fluxo completo

1. **Componente React** chama `api.getMedicos()`
2. `api.getMedicos()` faz `fetch('/medicos/')`
3. **Browser** envia a requisição para `http://localhost:3000/medicos/` (mesma origem ✓)
4. **React dev server** intercepta a requisição via `setupProxy.js`
5. **Proxy** identifica que é `/medicos` e redireciona para `http://localhost:8001/medicos/`
6. **Backend de médicos** (porta 8001) processa e retorna os dados
7. **Proxy** retorna a resposta para o React dev server
8. **Browser** recebe a resposta com os dados ✓


### Resumo: Arquivos importantes

| Arquivo | O que faz |
|---------|-----------|
| `src/setupProxy.js` | Define as regras de redirecionamento (qual rota vai para qual porta) |
| `src/api.js` | Centraliza todas as requisições usando caminhos relativos (`/medicos/`, `/agendas/`, etc.) |
| Componentes (`components/paginas/*.js`) | Usam `api.js` para fazer requisições, sem se preocupar com portas |



