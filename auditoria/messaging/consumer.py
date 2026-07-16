import json

from .rabbitmq import criar_conexao


def iniciar_consumidor():
    conexao = criar_conexao()
    canal = conexao.channel()

    canal.exchange_declare(
        exchange="agendamentos",
        exchange_type="fanout",
        durable=True,
    )

    fila = canal.queue_declare(
        queue="fila_auditoria",
        durable=True,
    )

    nome_fila = fila.method.queue

    canal.queue_bind(
        exchange="agendamentos",
        queue=nome_fila,
    )

    def callback(ch, method, properties, body):
        evento = json.loads(body)

        print("[AUDITORIA] Evento recebido:")
        print(evento)

    canal.basic_consume(
        queue=nome_fila,
        on_message_callback=callback,
        auto_ack=True,
    )

    print("[AUDITORIA] Consumidor aguardando mensagens...")

    canal.start_consuming()