# Generated by Django 5.0.7 on 2024-09-05 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categoria_audioyvideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'categoria_audioyvideo',
                'verbose_name_plural': 'categoria_audioyvideos',
            },
        ),
        migrations.CreateModel(
            name='audioyvideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('details', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='audioyvideo')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audioyvideo.categoria_audioyvideo')),
            ],
            options={
                'verbose_name': 'audioyvideo',
                'verbose_name_plural': 'audioyvideos',
            },
        ),
    ]
