from django.db import models
from django.conf import settings
from audioyvideo.models import audioyvideo
from componentes.models import componentes
from equipos.models import equipos
from redes.models import redes
import random
import string

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Carrito de {self.usuario}'

    def calcular_total(self):
        total = sum(
            item.cantidad * (
                item.producto_audioyvideo.price if item.producto_audioyvideo else
                item.producto_componentes.price if item.producto_componentes else
                item.producto_equipos.price if item.producto_equipos else
                item.producto_redes.price if item.producto_redes else 0
            )
            for item in self.items.all()
        )
        return total

    def save(self, *args, **kwargs):
        # Primero guarda el carrito sin el total
        super().save(*args, **kwargs)
        # Ahora calcula el total y actualiza el carrito
        self.total = self.calcular_total()
        super().save(update_fields=['total'])


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto_audioyvideo = models.ForeignKey(audioyvideo, blank=True, null=True, on_delete=models.CASCADE)
    producto_componentes = models.ForeignKey(componentes, blank=True, null=True, on_delete=models.CASCADE)
    producto_equipos = models.ForeignKey(equipos, blank=True, null=True, on_delete=models.CASCADE)
    producto_redes = models.ForeignKey(redes, blank=True, null=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.get_producto_name()}'

    def get_producto_name(self):
        if self.producto_audioyvideo:
            return self.producto_audioyvideo.name
        elif self.producto_componentes:
            return self.producto_componentes.name
        elif self.producto_equipos:
            return self.producto_equipos.name
        elif self.producto_redes:
            return self.producto_redes.name
        return 'Producto desconocido'

    def get_producto_price(self):
        if self.producto_audioyvideo:
            return self.producto_audioyvideo.price
        elif self.producto_componentes:
            return self.producto_componentes.price
        elif self.producto_equipos:
            return self.producto_equipos.price
        elif self.producto_redes:
            return self.producto_redes.price
        return 0

    def get_producto_image_url(self):
        if self.producto_audioyvideo:
            return self.producto_audioyvideo.image.url if self.producto_audioyvideo.image else ''
        elif self.producto_componentes:
            return self.producto_componentes.image.url if self.producto_componentes.image else ''
        elif self.producto_equipos:
            return self.producto_equipos.image.url if self.producto_equipos.image else ''
        elif self.producto_redes:
            return self.producto_redes.image.url if self.producto_redes.image else ''
        return ''

class Recibo(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recibo_codigo = models.CharField(max_length=10, blank=True, null=True, unique=True)
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    def generate_recibo_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def save(self, *args, **kwargs):
        if not self.recibo_codigo: 
            unique_code = False
            while not unique_code:
                new_code = self.generate_recibo_code()
                if not Recibo.objects.filter(recibo_codigo=new_code).exists():
                    self.recibo_codigo = new_code
                    unique_code = True
        super().save(*args, **kwargs)



class Vendidos(models.Model):
    producto_name= models.CharField(max_length=50)
    producto_price= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    producto_quantity= models.IntegerField(default=0)
    producto_state= models.BooleanField(default=False)
    producto_codigo= models.CharField(max_length=10, blank=True, null=True)
    producto_compra=models.BooleanField(default=False)
