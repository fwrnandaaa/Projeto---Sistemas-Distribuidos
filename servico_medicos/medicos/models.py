from django.db import models

# Create your models here.
class Especialidade(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=200)
    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.ForeignKey(Especialidade,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.nome