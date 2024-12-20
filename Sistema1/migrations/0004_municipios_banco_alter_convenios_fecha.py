# Generated by Django 4.2.3 on 2024-12-15 03:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema1', '0003_notificaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipios',
            name='banco',
            field=models.CharField(choices=[('BANCOESTADO', 'BANCOESTADO'), ('BANCODECHILE', 'BANCODECHILE'), ('BANCOINTERNACIONAL', 'BANCOINTERNACIONAL'), ('SCOTIABANK', 'SCOTIABANK'), ('BCI', 'BCI'), ('CORPBANCA', 'CORPBANCA'), ('BICE', 'BICE'), ('SANTANDER', 'SANTANDER'), ('ITAU', 'ITAU'), ('FALABELLA', 'FALABELLA'), ('RIPLEY', 'RIPLEY'), ('CONSORCIO', 'CONSORCIO'), ('BBVA', 'BBVA'), ('COOPEUCH', 'COOPEUCH'), ('LOSHEROES', 'LOSHEROES'), ('MERCADOPAGO', 'MERCADOPAGO')], default='BANCOESTADO', max_length=200),
        ),
        migrations.AlterField(
            model_name='convenios',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
