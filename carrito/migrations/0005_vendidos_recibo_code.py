# Generated by Django 5.0.7 on 2024-09-14 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0004_vendidos'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendidos',
            name='recibo_code',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]
