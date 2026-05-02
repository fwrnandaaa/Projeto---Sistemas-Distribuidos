from django.contrib import admin

from .models import Agenda, Agendamento

admin.site.register(Agendamento)
admin.site.register(Agenda)