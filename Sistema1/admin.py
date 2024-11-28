from django.contrib import admin
from .models import Convenios, Municipios, HistorialConvenios
# Register your models here.
admin.site.register(Convenios)
admin.site.register(Municipios)
admin.site.register(HistorialConvenios)

