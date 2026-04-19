from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Agendamento, Agenda

class AgendaSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Agenda
        fields = ['id', 'medico_id', 'data', 'horario', 'disponivel', '_links']

    def get__links(self, obj):
        request = self.context.get('request')
        return {
            "self": reverse('agenda-detail', args=[obj.pk], request=request),
        }

class AgendamentoSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    # para visualização da agenda associada
    agenda_detalhe = AgendaSerializer(source='agenda', read_only=True)

    class Meta:
        model = Agendamento
        # 'agenda' (ID) para salvar; 'agenda_detalhe' (objeto) para visualizar
        fields = ['id', 'usuario_cpf', 'agenda', 'agenda_detalhe', '_links']

    def get__links(self, obj):
        request = self.context.get('request')
        return {
            "self": reverse('agendamento-detail', args=[obj.pk], request=request),
        }