"""
Funções simples para controlar os clientes conectados via WebSocket.

Este arquivo concentra a lógica de gerenciamento dos clientes
e o envio de mensagens para todos eles, chamado de broadcast.
"""

from __future__ import annotations

from typing import Any
from fastapi import WebSocket


# Conjunto global com os clientes WebSocket conectados.
active_connections: set[WebSocket] = set()


async def add_connection(websocket: WebSocket) -> None:
    """Aceita e registra uma nova conexão WebSocket."""
    await websocket.accept()
    active_connections.add(websocket)


def remove_connection(websocket: WebSocket) -> None:
    """Remove uma conexão WebSocket encerrada."""
    active_connections.discard(websocket)


def count_connections() -> int:
    """Retorna a quantidade atual de clientes conectados."""
    return len(active_connections)


async def broadcast(message: dict[str, Any]) -> int:
    """Envia uma mensagem JSON para todos os clientes conectados."""
    delivered = 0

    for websocket in list(active_connections):
        try:
            await websocket.send_json(message)
            delivered += 1
        except Exception:
            remove_connection(websocket)

    return delivered