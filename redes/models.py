from django.db import models

# Create your models here.
class categoria_redes(models.Model):
    name= models.CharField(max_length=50)
    created= models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now_add=True)
    class Meta:
        verbose_name='categoria_redes'
        verbose_name_plural='categoria_redes'
    def __str__(self):
        return self.name

class redes(models.Model):
    name= models.CharField(max_length=50)
    price= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    details=models.CharField(max_length=255)
    quantity=models.IntegerField(default=0)
    category = models.ForeignKey(categoria_redes, on_delete=models.CASCADE)
    image=models.ImageField( upload_to='redes')
    state = models.BooleanField(default=False)
    created= models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name='redes'
        verbose_name_plural='redes'
    def __str__(self):
        return self.name