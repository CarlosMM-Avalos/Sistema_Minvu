from django.contrib import admin
from .models import Convenios, Municipios, HistorialConvenios,Rendiciones,Programas,Notificaciones,Reintegros
# Register your models here.
admin.site.register(Programas)
admin.site.register(Convenios)
admin.site.register(Municipios)
admin.site.register(HistorialConvenios)
admin.site.register(Rendiciones)
admin.site.register(Notificaciones)
admin.site.register(Reintegros)
