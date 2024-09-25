from django.contrib import admin

# Register your models here.
from .models import categoria_equipos, equipos


class equipoAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class categoriaEquiposAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')    
admin.site.register(equipos, equipoAdmin)
admin.site.register(categoria_equipos,categoriaEquiposAdmin)