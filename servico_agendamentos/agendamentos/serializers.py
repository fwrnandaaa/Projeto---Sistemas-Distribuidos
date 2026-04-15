from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Usuario, Agendamento, Agenda

class UsuarioSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'telefone', 'cpf', 'data_nascimento', '_links']

    def get__links(self, obj):
        request = self.context.get('request')
        return {
            "self": reverse('usuario-detail', args=[obj.pk], request=request),
        }

class AgendaSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()
    class Meta:
        model = Agenda
        fields = ['medico_id', 'data', 'horario', 'disponivel', '_links']

    def get__links(self, obj):
        request = self.context.get('request')
        return {
            "self": reverse('agenda-detail', args=[obj.pk], request=request),
        }

class AgendamentoSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()
    
    #para visualização dos dados já agendados 
    usuario_detalhe = UsuarioSerializer(source='usuario', read_only=True)
    agenda_detalhe = AgendaSerializer(source='agenda', read_only=True)

    class Meta:
        model = Agendamento
        # 'usuario' e 'agenda' (IDs) para salvar
        # 'usuario_detalhe' e 'agenda_detalhe' (Objetos) para ver
        fields = ['id', 'usuario', 'agenda', 'usuario_detalhe', 'agenda_detalhe', '_links']

    def get__links(self, obj):
        request = self.context.get('request')
        return {
            "self": reverse('agendamento-detail', args=[obj.pk], request=request),
        }