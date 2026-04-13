from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Medico, Especialidade

class EspecialidadeSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Especialidade
        fields = ['id', 'nome', '_links']

    def get__links(self, obj):
        request = self.context.get('request')
        return {
            "self": reverse('especialidade-detail', args=[obj.pk], request=request),
        }


class MedicoSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()
    especialidade_detalhe = EspecialidadeSerializer(source='especialidade', read_only=True)
    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'especialidade', 'especialidade_detalhe', '_links']


    def get__links(self, obj):
        request = self.context.get('request')
        links = {
            "self": reverse('medico-detail', args=[obj.pk], request=request),
        }
        if obj.especialidade:
            links["especialidade"] = reverse(
                'especialidade-detail',
                args=[obj.especialidade.pk],
                request=request
            )
        return links