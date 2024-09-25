from django.urls import path
from . import views

urlpatterns = [
    path('',views.mostrar_equipos, name='equipos'),
    path('state/<int:producto_id>/', views.agregar_carrito, name='state_equipos'),
    path('producto/<int:producto_id>/', views.detail_product, name='details_e'),
    path('update/<int:producto_id>', views.actualizar_carrito, name='actualizar_carrito_e'),
    path('eliminar_equipos/<int:producto_id>/', views.eliminar_del_carrito_equipos, name='eliminar_del_carrito_equipos'),
    path('categoria/<int:categoria_id>',views.filtro_equipos, name='filtrar_por_categoria_e'),
]
