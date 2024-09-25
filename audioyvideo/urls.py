from django.urls import path
from . import views
urlpatterns = [
    path('',views.mostrar_audioyvideo, name='audioyvideo'),
    path('state/<int:producto_id>/', views.agregar_carrito, name='state_audioyvideo'),
    path('eliminar_audioyvideo/<int:producto_id>/', views.eliminar_del_carrito_audioyvideo, name='eliminar_del_carrito_audioyvideo'),
    path('producto/<int:producto_id>/', views.detail_product, name='details_a'),
    path('update/<int:producto_id>', views.actualizar_carrito, name='actualizar_carrito_a'),
    path('categoria/<int:categoria_id>/', views.filtro_audioyvideo, name='filtrar_por_categoria_a'),
]
