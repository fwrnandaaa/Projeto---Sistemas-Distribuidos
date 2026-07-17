import asyncio
import json

from broadcaster import broadcast
from .rabbitmq import criar_conexao


def iniciar_consumidor(loop):
    conexao = criar_conexao()
    canal = conexao.channel()

    canal.exchange_declare(
        exchange="agendamentos",
        exchange_type="fanout",
        durable=True,
    )

    fila = canal.queue_declare(
    queue="fila_websocket",
    durable=True, 
    )
    
    nome_fila = fila.method.queue

    canal.queue_bind(
        exchange="agendamentos",
        queue=nome_fila,
    )

    def callback(ch, method, properties, body):
        evento = json.loads(body)

        print("[MOM] Evento recebido:")
        print(evento)

        asyncio.run_coroutine_threadsafe(
            broadcast(evento),
            loop,
)

    canal.basic_consume(
        queue=nome_fila,
        on_message_callback=callback,
        auto_ack=True,
    )

    print("[MOM] Consumidor aguardando mensagens...")
    canal.start_consuming()