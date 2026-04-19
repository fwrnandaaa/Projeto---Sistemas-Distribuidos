from django.db import models

# Create your models here.

class Agenda(models.Model):
    medico_id = models.PositiveIntegerField()
    data = models.DateField()
    horario = models.TimeField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        status = "Disponível" if self.disponivel else "Indisponível"
        return f"Medico ID: {self.medico_id} - {self.data} {self.horario} - {status}"

class Agendamento(models.Model):
    usuario_cpf = models.CharField(max_length=14)
    agenda = models.OneToOneField(Agenda, on_delete=models.CASCADE)

    def __str__(self):
        return f"CPF: {self.usuario_cpf} - {self.agenda.data} {self.agenda.horario}"
