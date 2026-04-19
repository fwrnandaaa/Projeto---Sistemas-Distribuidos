from rest_framework import viewsets
from .models import Agendamento, Agenda
from .serializers import AgendamentoSerializer, AgendaSerializer

# Create your views here.

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
