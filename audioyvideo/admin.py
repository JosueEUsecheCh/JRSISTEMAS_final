from django.contrib import admin

# Register your models here.
from .models import categoria_audioyvideo, audioyvideo


class audioVideoAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class categoriaAudioVideoAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')    
admin.site.register(audioyvideo,audioVideoAdmin)
admin.site.register(categoria_audioyvideo,categoriaAudioVideoAdmin)