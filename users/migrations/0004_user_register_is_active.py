# Generated by Django 5.0.7 on 2024-09-09 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_register_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_register',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
