# Serviço de Notificações WebSocket

Microserviço responsável pela comunicação em tempo real utilizando WebSocket.

O objetivo deste serviço é demonstrar o funcionamento de conexões persistentes, envio de mensagens em tempo real e distribuição de eventos para múltiplos clientes conectados simultaneamente.

Este serviço foi implementado de forma independente da arquitetura REST existente, atuando como um componente especializado em notificações em tempo real.

Atualmente, ele não está integrado ao gateway, frontend React ou serviço de agendamentos. Entretanto, sua estrutura já está preparada para receber eventos desses serviços futuramente.

## Porta

O serviço deve rodar na porta `8004`.

## Como executar

A partir da raiz do projeto:

```powershell
cd websocket_notificacoes
uvicorn server:app --reload --port 8004
```

Também é possível executar diretamente:

```powershell
cd websocket_notificacoes
python server.py
```

## Estrutura

```text
websocket_notificacoes/
├── server.py
├── broadcaster.py
├── painel_websocket.html
└── README.md
```

### Responsabilidades dos arquivos

#### server.py

Responsável pelo ciclo de vida das conexões WebSocket:

* inicialização do serviço;
* aceitação de novas conexões;
* recebimento de mensagens;
* registro de eventos no console;
* encaminhamento de mensagens para broadcast.

#### broadcaster.py

Responsável pelo gerenciamento dos clientes conectados:

* armazenamento das conexões ativas;
* remoção de conexões encerradas;
* contagem de clientes conectados;
* envio de mensagens para todos os clientes simultaneamente (broadcast).

#### painel_websocket.html

Interface simples utilizada para testes e demonstração da atividade.

Permite:

* conectar ao servidor WebSocket;
* enviar mensagens;
* visualizar mensagens recebidas em tempo real;
* simular múltiplos clientes abrindo mais de uma aba do navegador.

## Endpoints

| Tipo      | Rota                 | Descrição                                                          |
| --------- | -------------------- | ------------------------------------------------------------------ |
| HTTP      | `GET /health`        | Verifica o status do serviço e a quantidade de clientes conectados |
| HTTP      | `POST /notificacoes` | Publica uma notificação manual para todos os clientes conectados   |
| WebSocket | `/ws/notificacoes`   | Canal de comunicação em tempo real                                 |

## Interface de teste

Abra o arquivo `painel_websocket.html` em duas abas do navegador.

A interface estabelece conexão com:

```text
ws://localhost:8004/ws/notificacoes
```

Cada aba representa um cliente WebSocket independente.

As mensagens enviadas por qualquer cliente serão distribuídas automaticamente para todos os clientes conectados.

## Exemplo de publicação manual

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8004/notificacoes `
  -ContentType "application/json" `
  -Body '{"tipo":"teste","mensagem":"Servico WebSocket funcionando","dados":{}}'
```

## Exemplo de mensagem WebSocket

```json
{
  "tipo": "novo_agendamento",
  "dados": {
    "medico": "Dr. João",
    "data": "10/06",
    "hora": "14:00"
  }
}
```

## Fluxo de funcionamento

```text
Cliente A
      │
      ▼
WebSocket
      │
      ├────► Cliente A
      ├────► Cliente B
      └────► Cliente C
```

Quando uma mensagem é recebida pelo servidor, ela é enviada para todos os clientes conectados por meio do mecanismo de broadcast.

## Possíveis integrações futuras

O serviço foi projetado para receber eventos gerados por outros componentes do sistema, como:

* novo agendamento criado;
* agendamento cancelado;
* agenda criada ou removida;
* médico atualizado;
* alteração de disponibilidade.

Nesses cenários, o gateway ou o serviço de agendamentos poderá publicar um evento para este microserviço, que ficará responsável por distribuir a atualização em tempo real para todos os clientes conectados.
