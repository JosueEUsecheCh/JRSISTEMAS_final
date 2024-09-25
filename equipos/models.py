from django.db import models

# Create your models here.
class categoria_equipos(models.Model):
    name= models.CharField(max_length=50)
    created= models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now_add=True)
    class Meta:
        verbose_name='categoria_equipo'
        verbose_name_plural='categoria_equipos'
    def __str__(self):
        return self.name

class equipos(models.Model):
    name= models.CharField(max_length=50)
    price= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    details=models.CharField(max_length=500)
    quantity=models.IntegerField(default=0)
    category = models.ForeignKey(categoria_equipos, on_delete=models.CASCADE)
    image=models.ImageField( upload_to='equipos')
    state = models.BooleanField(default=False)
    created= models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name='equipo'
        verbose_name_plural='equipos'
    def __str__(self):
        return self.name