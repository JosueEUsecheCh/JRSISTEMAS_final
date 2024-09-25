from django.db import models

# Create your models here.
class categoria_Componentes(models.Model):
    name= models.CharField(max_length=50)
    created= models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now_add=True)
    class Meta:
        verbose_name='categoria_componente'
        verbose_name_plural='categoria_componentes'
    def __str__(self):
        return self.name

class componentes(models.Model):
    name= models.CharField(max_length=50)
    price= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    details=models.CharField(max_length=255)
    quantity=models.IntegerField(default=0)
    category = models.ForeignKey(categoria_Componentes, on_delete=models.CASCADE)
    image=models.ImageField( upload_to='componentes')
    state = models.BooleanField(default=False)
    created= models.DateField(auto_now_add=True)
    updated= models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)  

    class Meta:
        verbose_name='componente'
        verbose_name_plural='componentes'
    def __str__(self):
        return self.name