from django.urls import path
from . import views

urlpatterns = [
    path('',views.mostrar_redes,name='redes'),
    path('state/<int:producto_id>/', views.agregar_carrito, name='state_redes'),
    path('eliminar_redes/<int:producto_id>/', views.eliminar_del_carrito_redes, name='eliminar_del_carrito_redes'),
    path('producto/<int:producto_id>/', views.detail_product, name='details_r'),
    path('update/<int:producto_id>', views.actualizar_carrito, name='actualizar_carrito_r'),
    path('categoria/<int:categoria_id>',views.filtro_redes,name='filtrar_por_categoria_r'),
]
