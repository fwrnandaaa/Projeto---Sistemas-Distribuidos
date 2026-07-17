from rest_framework import viewsets
from .models import Agendamento, Agenda
from .serializers import AgendamentoSerializer, AgendaSerializer
# import requests
from servico_agendamentos.messaging.publisher import publicar_novo_agendamento


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def perform_create(self, serializer):
        agendamento = serializer.save()
        publicar_novo_agendamento(agendamento)