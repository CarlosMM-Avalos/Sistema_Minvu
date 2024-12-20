from django.db import models
from datetime import date
from django.utils import timezone
from datetime import datetime
# Create your models here.



class Programas(models.Model):
    nombre = models.CharField(max_length=255)  # Campo para el nombre del programa
    descripcion = models.TextField()  # Campo para la descripción del programa
    imagen = models.ImageField(upload_to='programas/')  # Campo para la imagen, con una ruta de carga

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'Programas'



class Municipios(models.Model):

    BANCOS_CHOICES = [
        ('BANCOESTADO', 'BANCOESTADO'),
        ('BANCODECHILE', 'BANCODECHILE'),
        ('BANCOINTERNACIONAL', 'BANCOINTERNACIONAL'),
        ('SCOTIABANK', 'SCOTIABANK'),
        ('BCI', 'BCI'),
        ('CORPBANCA', 'CORPBANCA'),
        ('BICE', 'BICE'),
        ('SANTANDER', 'SANTANDER'),
        ('ITAU', 'ITAU'),
        ('FALABELLA', 'FALABELLA'),
        ('RIPLEY', 'RIPLEY'),
        ('CONSORCIO', 'CONSORCIO'),
        ('BBVA', 'BBVA'),
        ('COOPEUCH', 'COOPEUCH'),
        ('LOSHEROES', 'LOSHEROES'),
        ('MERCADOPAGO', 'MERCADOPAGO'),]
    
    TCUENTA_CHOICES = [
        ('Cuenta_Corriente', 'Cuenta Corriente'),
        ('Cuenta_vista', 'Cuenta vista'),
        ('Cuenta_Rut', 'Cuenta Rut'),
        ('Cuenta_Ahorro', 'Cuenta Ahorro'),
        ('Otro', 'Otro'),
        ]
    
    programas = models.ForeignKey(Programas, blank=True, null=True, on_delete=models.CASCADE, related_name='municipios')
    nombre = models.CharField(max_length=50, verbose_name="Municipios")
    rut = models.CharField(max_length=20, verbose_name = "Rut")
    cuenta = models.CharField(max_length=50, verbose_name="Cuenta")
    banco = models.CharField(max_length=200,choices=BANCOS_CHOICES, default='BANCOESTADO',)
    tcuenta = models.CharField(max_length=200,choices=TCUENTA_CHOICES, default='Cuenta_Corriente',)
    class Meta:
        db_table = 'Municipios'


    def __str__(self):
        return f"{self.nombre} "


class Convenios(models.Model):
    municipio = models.ForeignKey(Municipios, blank=True, null=True, on_delete=models.CASCADE, related_name='convenios')
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    res = models.IntegerField(default=0)  # Valor predeterminado para filas existentes
    fecha = models.DateField(default=timezone.now)
    lcl = models.CharField(max_length=200, default='Desconocido')  # Valor predeterminado para filas existentes
    total = models.IntegerField()
    documento = models.FileField(upload_to='convenios/')

    

    def save(self, *args, **kwargs):
        # Asegurar que `fecha` sea del tipo datetime.date
        if isinstance(self.fecha, str):
            self.fecha = datetime.strptime(self.fecha, "%Y-%m-%d").date()

        # Verificar si la fecha está en el pasado
        if self.fecha < timezone.now().date():
            mensaje = f"El convenio '{self.nombre}' tiene una fecha superada: {self.fecha}"
            Notificaciones.objects.create(mensaje=mensaje)
        
        # Llamar al método `save` del padre
        super().save(*args, **kwargs)

    
    class Meta:
        db_table = 'Convenios'

    def __str__(self):
        return f"{self.nombre} "



class HistorialConvenios(models.Model):
  
    convenio_madre = models.ForeignKey(Convenios, related_name='historial', on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    res = models.IntegerField(default=0)  # Valor predeterminado para filas existentes
    fecha = models.DateField(default=date(2024, 1, 1))
    lcl = models.CharField(max_length=200, default='Desconocido')
    total = models.IntegerField()
    documento = models.FileField(upload_to='historial_convenios/', blank=True, null=True)

    class Meta:
        db_table = 'HistorialConvenios'
        ordering = ['-fecha_modificacion']

    def __str__(self):
        return f"Historial de {self.convenio_madre.nombre} ({self.fecha_modificacion})"
    


class Rendiciones(models.Model):

    ESTADO_CHOICES = [
        ('rendido', 'Rendido'),
        ('sin_rendir', 'Sin Rendir'),
        ('cancelado', 'Cancelado'),
    ]

    MES_CHOICES = [
        ('enero', 'Enero'),
        ('febrero', 'Febrero'),
        ('marzo', 'Marzo'),
        ('abril', 'abril'),
        ('mayo', 'Mayo'),
        ('junio', 'Junio'),
        ('julio', 'Julio'),
        ('agosto', 'Agosto'),
        ('septiembre', 'Septiembre'),
        ('octubre', 'Octubre'),
        ('noviembre', 'Noviembre'),
        ('diciembre', 'Diciembre'),

    ]

    
    convenio = models.ForeignKey(Convenios, blank=True, null=True, on_delete=models.CASCADE,)
    descripcion =models.TextField(max_length=5000,blank=True, )
    mes_rendicion = models.CharField(max_length=200,choices=MES_CHOICES, default='enero',)
    numero_oficio = models.IntegerField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='sin_rendir', )
    fecha_de_oficio = models.DateField(max_length=200)
    n_nemo_interno = models.IntegerField()
    n_sigfe = models.IntegerField()
    fecha_sigfe = models.DateField(max_length=200)
    fecha_actual = models.DateField(max_length=200)
    gasto_operacional = models.IntegerField()
    gasto_personal = models.IntegerField()
    gasto_inversion = models.IntegerField()


    class Meta:
        db_table = 'Rendiciones'
    
    def __str__(self):
        return str(self.numero_oficio)  # convertida en string


class Notificaciones(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    
    def __str__(self):
        return self.mensaje


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Reintegros(models.Model):
    ESTADO_CHOICES = [
        ('reintegrado', 'Reintegrado'),
        ('sin_reintegrar', 'Sin Reintegrar'),
        ('cancelado', 'Cancelado'),
    ]
    
    convenio = models.ForeignKey(Convenios,blank=True,null=True,on_delete=models.CASCADE,help_text="Convenio relacionado con el reintegro."    )
    fecha_solicitud = models.DateField(help_text="Fecha en que se solicitó el reintegro.")
    fecha_aprobacion = models.DateField(help_text="Fecha en que se aprobó el reintegro.")
    codigo_referencia = models.CharField(max_length=255,help_text="Código único de referencia del reintegro.")
    numero_oficio = models.IntegerField(help_text="Número de oficio relacionado.")
    fecha_oficio = models.DateField(help_text="Fecha del oficio.")
    numero_sigfe = models.IntegerField(help_text="Número asociado en SIGFE.")
    fecha_sigfe = models.DateField(help_text="Fecha asociada en SIGFE.")
    monto_entregado = models.IntegerField(help_text="Monto entregado inicialmente."    )
    monto_reintegrar = models.IntegerField( help_text="Monto que debe reintegrarse."    )
    descripcion = models.TextField(max_length=5000,blank=True,help_text="Descripción o detalle del reintegro."    )
    fecha_creacion = models.DateField(auto_now_add=True,help_text="Fecha en que se creó el registro."    )
    fecha_limite_devolucion = models.DateField(help_text="Fecha límite para la devolución del monto."    )
    estado_reintegro = models.CharField(max_length=20,choices=ESTADO_CHOICES,default='sin_reintegrar',help_text="Estado actual del reintegro."    )
    documento = models.FileField(upload_to='reintegros/',blank=True,null=True,help_text="Documento adjunto relacionado con el reintegro."    )

    class Meta:
        db_table = 'Reintegros'

    def __str__(self):
        return f"Reintegro {self.codigo_referencia} - {self.get_estado_reintegro_display()}"
