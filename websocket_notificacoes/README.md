# Serviço de Notificações WebSocket

Microserviço responsável pela comunicação em tempo real utilizando o protocolo WebSocket.

O objetivo deste serviço é demonstrar o funcionamento de conexões persistentes, envio de mensagens em tempo real e distribuição de eventos para múltiplos clientes conectados simultaneamente.

Este serviço atua como um componente especializado em notificações em tempo real dentro da arquitetura do sistema de agendamento de consultas.

Atualmente, ele está integrado ao frontend React e ao serviço de agendamentos, permitindo que novos agendamentos gerem notificações automaticamente para todos os clientes conectados.

---

## Porta

O serviço deve ser executado na porta:

```text
8004
```

---

## Como executar

A partir da raiz do projeto:

```powershell
cd websocket_notificacoes
uvicorn server:app --reload --port 8004
```

---

## Estrutura

```text
websocket_notificacoes/
├── __init__.py
├── server.py
├── broadcaster.py
└── README.md
```

---

## Responsabilidades dos arquivos

### server.py

Responsável pelo ciclo de vida das conexões WebSocket.

Principais responsabilidades:

* inicializar o serviço;
* aceitar novas conexões;
* receber mensagens;
* registrar eventos no console;
* disponibilizar endpoints HTTP auxiliares;
* encaminhar mensagens para broadcast.

---

### broadcaster.py

Responsável pelo gerenciamento dos clientes conectados.

Principais responsabilidades:

* armazenar conexões ativas;
* remover conexões encerradas;
* contabilizar clientes conectados;
* enviar mensagens para todos os clientes simultaneamente (broadcast).

---

## Endpoints

| Tipo      | Rota                 | Descrição                                                          |
| --------- | -------------------- | ------------------------------------------------------------------ |
| HTTP      | `GET /health`        | Verifica o status do serviço e a quantidade de clientes conectados |
| HTTP      | `POST /notificacoes` | Publica uma notificação para todos os clientes conectados          |
| WebSocket | `/ws/notificacoes`   | Canal de comunicação em tempo real                                 |

---

## Health Check

O endpoint:

```text
GET /health
```

permite verificar se o serviço está ativo.

Exemplo de resposta:

```json
{
  "status": "ok",
  "clientes_conectados": 2
}
```

---

## Publicação manual de notificações

Para testes, é possível publicar notificações manualmente utilizando:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8004/notificacoes `
  -ContentType "application/json" `
  -Body '{"tipo":"teste","mensagem":"Servico WebSocket funcionando","dados":{}}'
```

---

## Exemplo de mensagem

Exemplo de evento enviado para os clientes conectados:

```json
{
  "tipo": "novo_agendamento",
  "dados": {
    "medico_id": 4,
    "data": "2026-07-04",
    "horario": "12:00:00"
  }
}
```

---

## Integração implementada

Atualmente o serviço recebe notificações geradas pelo serviço de agendamentos.

Quando um novo agendamento é criado:

1. O frontend envia uma requisição para o serviço de agendamentos.
2. O serviço de agendamentos salva o novo registro.
3. O serviço de agendamentos envia uma notificação para o microserviço WebSocket.
4. O microserviço WebSocket realiza broadcast para todos os clientes conectados.
5. O frontend recebe a atualização automaticamente, sem necessidade de recarregar a página.

---

## Fluxo de funcionamento

```text
Frontend React
        │
        ▼
POST /agendamentos
        │
        ▼
Serviço de Agendamentos
        │
        ▼
POST /notificacoes
        │
        ▼
WebSocket
        │
        ├────► Cliente A
        ├────► Cliente B
        └────► Cliente C
```

---

## Requisitos atendidos

A implementação atende aos requisitos da atividade:

* utilização explícita do protocolo WebSocket (`ws://`);
* comunicação bidirecional entre cliente e servidor;
* envio de mensagens do servidor para todos os clientes conectados (broadcast);
* suporte a múltiplos clientes simultâneos;
* atualização automática da interface;
* registro de abertura de conexão;
* registro de recebimento de mensagens;
* registro de encerramento de conexão.



