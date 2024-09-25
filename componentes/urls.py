from django.urls import path
from . import views

urlpatterns = [
    path('',views.mostrar_componentes, name='componentes'),
    path('state/<int:producto_id>/', views.agregar_carrito, name='state_componentes'),
    path('eliminar_componentes/<int:producto_id>/', views.eliminar_del_carrito_componentes, name='eliminar_del_carrito_componentes'),
    path('producto/<int:producto_id>/', views.detail_product, name='details_c'),
    path('update/<int:producto_id>', views.actualizar_carrito, name='actualizar_carrito_c'),
    path('categoria/<int:categoria_id>/', views.filtro_componentes, name='filtrar_por_categoria'),
]
