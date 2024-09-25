# Generated by Django 5.0.7 on 2024-09-11 02:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('audioyvideo', '0002_audioyvideo_state'),
        ('componentes', '0002_componentes_state'),
        ('equipos', '0002_equipos_state'),
        ('redes', '0002_redes_state'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('audioyvideo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='audioyvideo.audioyvideo')),
                ('componentes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='componentes.componentes')),
                ('equipos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipos.equipos')),
                ('redes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='redes.redes')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
