from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    agenda = models.OneToOneField(Agenda, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.nome} - {self.agenda.data} {self.agenda.horario}"

class Agenda(models.Model):
    medico_id = models.PositiveIntegerField()
    data = models.DateField()
    horario = models.TimeField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        status = "Disponível" if self.disponivel else "Indisponível"
        return f"Medico ID: {self.medico_id} - {self.data} {self.horario} - {status}"
