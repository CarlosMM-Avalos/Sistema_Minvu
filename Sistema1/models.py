from django.db import models

# Create your models here.


class Municipio(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Municipio")
    rut = models.CharField(max_length=20, verbose_name = "Rut")
    cuenta = models.CharField(max_length=50, verbose_name="Cuenta")
    