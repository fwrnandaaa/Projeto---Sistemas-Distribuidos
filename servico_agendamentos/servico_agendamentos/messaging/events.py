def criar_evento_novo_agendamento(agendamento):
    return {
        "tipo": "novo_agendamento",
        "dados": {
            "agendamento_id": agendamento.id,
            "usuario_cpf": agendamento.usuario_cpf,
            "medico_id": agendamento.agenda.medico_id,
            "data": str(agendamento.agenda.data),
            "horario": str(agendamento.agenda.horario),
        }
    }