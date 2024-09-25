from django.contrib import admin

# Register your models here.
from .models import categoria_redes, redes


class redesAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class categoriaredesAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')    
admin.site.register(redes, redesAdmin)
admin.site.register(categoria_redes, categoriaredesAdmin)