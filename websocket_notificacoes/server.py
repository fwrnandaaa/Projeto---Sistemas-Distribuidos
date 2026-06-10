"""
Módulo responsável pelo ciclo de vida das conexões WebSocket.

Este arquivo inicializa o serviço de notificações em tempo real,
aceita conexões WebSocket, recebe mensagens dos clientes e encaminha
essas mensagens para todos os clientes conectados por meio do broadcast.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

try:
    from .broadcaster import (
        add_connection,
        broadcast,
        count_connections,
        remove_connection,
    )
except ImportError:
    from broadcaster import (
        add_connection,
        broadcast,
        count_connections,
        remove_connection,
    )


app = FastAPI(
    title="Serviço de Notificações WebSocket",
    description="Microserviço para notificações em tempo real.",
    version="1.0.0",
)


class NotificationPayload(BaseModel):
    """Modelo dos dados recebidos pela rota HTTP de publicação."""

    tipo: str = Field(default="notificacao", min_length=1)
    mensagem: str = Field(..., min_length=1)
    dados: dict[str, Any] = Field(default_factory=dict)


def build_event(tipo: str, dados: dict[str, Any]) -> dict[str, Any]:
    """Monta o formato padrão das mensagens enviadas aos clientes."""
    return {
        "tipo": tipo,
        "dados": dados,
        "enviado_em": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
async def health() -> dict[str, Any]:
    """Verifica se o serviço está ativo."""
    return {
        "status": "ok",
        "clientes_conectados": count_connections(),
    }


@app.post("/notificacoes")
async def publicar_notificacao(payload: NotificationPayload) -> dict[str, Any]:
    """
    Recebe uma notificação via HTTP e envia para todos os clientes WebSocket.

    Essa rota poderá ser chamada futuramente pelo gateway ou pelo serviço
    de agendamentos quando um novo agendamento for criado.
    """
    evento = build_event(
        payload.tipo,
        {
            "mensagem": payload.mensagem,
            "dados": payload.dados,
        },
    )

    entregues = await broadcast(evento)

    print(f"Notificação publicada via HTTP: {evento}")
    print(f"Clientes que receberam a notificação: {entregues}")

    return {
        "entregues": entregues,
        "evento": evento,
    }


@app.websocket("/ws/notificacoes")
async def websocket_notificacoes(websocket: WebSocket) -> None:
    """Controla uma conexão WebSocket com um cliente."""
    cliente_id = str(uuid4())

    await add_connection(websocket)

    print(f"Conexão aberta: cliente {cliente_id}")
    print(f"Clientes conectados: {count_connections()}")

    await websocket.send_json(
        build_event(
            "conexao",
            {
                "cliente_id": cliente_id,
                "mensagem": "Cliente conectado ao WebSocket.",
            },
        )
    )

    try:
        while True:
            texto_recebido = await websocket.receive_text()

            print(f"Mensagem recebida do cliente {cliente_id}: {texto_recebido}")

            try:
                dados_recebidos = json.loads(texto_recebido)
            except json.JSONDecodeError:
                dados_recebidos = {
                    "mensagem": texto_recebido,
                }

            evento = build_event(
                "mensagem_cliente",
                {
                    "cliente_id": cliente_id,
                    "conteudo": dados_recebidos,
                },
            )

            await broadcast(evento)

    except WebSocketDisconnect:
        remove_connection(websocket)

        print(f"Conexão encerrada: cliente {cliente_id}")
        print(f"Clientes conectados: {count_connections()}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
    )