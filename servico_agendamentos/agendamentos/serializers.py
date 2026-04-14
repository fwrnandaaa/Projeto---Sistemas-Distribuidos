from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Usuario, Agendamento, Agenda

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__' #ALTERAR

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__' #ALTERAR

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__' #ALTERAR