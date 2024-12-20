# Generated by Django 4.2.3 on 2024-12-14 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema1', '0002_historialconvenios_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('leido', models.BooleanField(default=False)),
            ],
        ),
    ]
