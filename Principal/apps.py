from django.apps import AppConfig


class PrincipalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Principal'

class ServiciotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicioT'
