from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.mostrar_producto, name='carrito'),
    path('pdf/', views.reports_pdf, name='pdf'),
    path('recibo/', views.recibo_correo , name='recibo'),
    
]
