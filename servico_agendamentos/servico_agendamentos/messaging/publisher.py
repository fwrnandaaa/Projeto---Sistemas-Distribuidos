from .events import criar_evento_novo_agendamento


def publicar_novo_agendamento(agendamento) -> None:
    evento = criar_evento_novo_agendamento(agendamento)

    print("[MOM] Evento preparado para publicação:")
    print(evento)