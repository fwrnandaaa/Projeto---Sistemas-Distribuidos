import json

from .events import criar_evento_novo_agendamento
from .rabbitmq import criar_conexao


def publicar_novo_agendamento(agendamento) -> None:
    evento = criar_evento_novo_agendamento(agendamento)

    conexao = criar_conexao()
    canal = conexao.channel()

    canal.exchange_declare(
        exchange="agendamentos",
        exchange_type="fanout",
        durable=True,
    )

    canal.basic_publish(
        exchange="agendamentos",
        routing_key="",
        body=json.dumps(evento),
    )

    conexao.close()

    print("[MOM] Evento publicado no RabbitMQ:")
    print(evento)