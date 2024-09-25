from django.contrib import admin

# Register your models here.
from .models import categoria_Componentes, componentes


class componenteAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class categoriaComponentesAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')    
admin.site.register(componentes, componenteAdmin)
admin.site.register(categoria_Componentes,categoriaComponentesAdmin)