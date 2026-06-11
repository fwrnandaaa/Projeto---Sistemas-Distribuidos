from rest_framework import viewsets
from .models import Agendamento, Agenda
from .serializers import AgendamentoSerializer, AgendaSerializer
import requests


def notificar_novo_agendamento(agendamento):
    try:
        payload = {
            "tipo": "novo_agendamento",
            "mensagem": "Novo agendamento criado",
            "dados": {
                "agendamento_id": agendamento.id,
                "usuario_cpf": agendamento.usuario_cpf,
                "medico_id": agendamento.agenda.medico_id,
                "data": str(agendamento.agenda.data),
                "horario": str(agendamento.agenda.horario),
            },
        }

        requests.post(
            "http://localhost:8004/notificacoes",
            json=payload,
            timeout=3,
        )

    except requests.RequestException as erro:
        print(f"Erro ao enviar notificação WebSocket: {erro}")


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def perform_create(self, serializer):
        agendamento = serializer.save()
        notificar_novo_agendamento(agendamento)