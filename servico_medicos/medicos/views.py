from django.shortcuts import render
from rest_framework import viewsets
from .models import Medico, Especialidade
from .serializers import MedicoSerializer, EspecialidadeSerializer
# Create your views here.

class EspecialidadeViewSet(viewsets.ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer