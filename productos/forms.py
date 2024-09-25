from django import forms
from componentes.models import categoria_Componentes
from equipos.models import categoria_equipos
from redes.models import categoria_redes
from audioyvideo.models import categoria_audioyvideo

class register_products(forms.Form):
    name = forms.CharField(
        label='Producto',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'name_product', 'placeholder': 'Nombre del producto'})
    )
       
    details = forms.CharField(
        label='Detalles',
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={'class': 'details_product', 'placeholder': 'Detalles del producto'})
    )

    image = forms.ImageField(
        required=True,
        label='Imagen',
        widget=forms.ClearableFileInput(attrs={'class': 'image_product'})
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=0,
        label='Precio',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'price_product',
            'placeholder': '0.00',
            'step': '0',
            'min': '0',
            'max': '99999999.99'
        })
    )
    
    quantity = forms.IntegerField(
        label='Cantidad',
        initial=1,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'quantity_product'})
    )
    
    category = forms.ChoiceField(
        #choices=[],
        label='Categoría',
        required=True,
        widget=forms.Select(attrs={'class': 'category_product'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categoria_choices = []

        # Obtener las opciones dinámicamente de los modelos de categoría
        categoria_choices += [(f'audio_{cat.id}', f'Audio y Video: {cat.name}') for cat in categoria_audioyvideo.objects.all()]
        categoria_choices += [(f'equipo_{cat.id}', f'Equipos: {cat.name}') for cat in categoria_equipos.objects.all()]
        categoria_choices += [(f'componente_{cat.id}', f'Componentes: {cat.name}') for cat in categoria_Componentes.objects.all()]
        categoria_choices += [(f'redes_{cat.id}', f'Redes: {cat.name}') for cat in categoria_redes.objects.all()]

        # Debug: Imprime las opciones de categoría para verificar
        print("Categorías cargadas:", categoria_choices)

        self.fields['category'].choices = categoria_choices

