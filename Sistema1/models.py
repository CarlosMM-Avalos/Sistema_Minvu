from django.db import models

# Create your models here.


class Municipios(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Municipios")
    rut = models.CharField(max_length=20, verbose_name = "Rut")
    cuenta = models.CharField(max_length=50, verbose_name="Cuenta")
    class Meta:
        db_table = 'Municipios'


    def __str__(self):
        return f"{self.nombre} "


class Convenios(models.Model):
    id = models.IntegerField(primary_key=True)
    municipio = models.ForeignKey(Municipios, blank=True, null=True, on_delete=models.CASCADE, related_name='convenios')
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    total = models.IntegerField()
    documento = models.FileField(upload_to='convenios/', )
    class Meta:
        db_table = 'Convenios'

    def __str__(self):
        return f"{self.nombre} "


class HistorialConvenios(models.Model):
    id = models.AutoField(primary_key=True)
    convenio_madre = models.ForeignKey(Convenios, related_name='historial', on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    total = models.IntegerField()
    documento = models.FileField(upload_to='historial_convenios/', blank=True, null=True)

    class Meta:
        db_table = 'HistorialConvenios'
        ordering = ['-fecha_modificacion']

    def __str__(self):
        return f"Historial de {self.convenio_madre.nombre} ({self.fecha_modificacion})"
