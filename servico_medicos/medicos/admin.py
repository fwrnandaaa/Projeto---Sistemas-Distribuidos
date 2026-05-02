from django.contrib import admin

from .models import Especialidade, Medico

admin.site.register(Medico)
admin.site.register(Especialidade)