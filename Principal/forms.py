from django import forms

class Contactanos(forms.Form):
    exposicion = forms.CharField(label='Asunto', widget=forms.Textarea)
    email = forms.EmailField(label='Correo Electrónico',required=True)
    SIZE_CHOICES=(
        ('Instalación de cámaras', 'Cámaras'),
        ('Mantenimiento de hardware', 'hardware'),
        ('Mantenimiento de software', 'software'),
        ('Revisión completa de equipo', 'Revisión de equipo'),
    )
    servicios=forms.CharField(choices=SIZE_CHOICES)