# Generated by Django 5.0.7 on 2024-09-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_register_is_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_register',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
