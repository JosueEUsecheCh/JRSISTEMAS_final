# Generated by Django 5.0.7 on 2024-09-11 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audioyvideo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audioyvideo',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]
