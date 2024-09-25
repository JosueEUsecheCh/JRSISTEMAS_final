from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('panelAdmin/',views.panel_admin,name='panel'),
    path('<int:id>/delete/', views.delete_products, name='eliminar'),
    path('update_products/<str:prefix>/<int:id>/', views.update_products, name='actualizar'),
    path('pdf/', views.reports_pdf, name='reports'),
    path('recibos/', views.listar_recibos, name='listar_recibos'),
    path('recibos/confirmar/<str:recibo_codigo>/', views.confirmar_compra, name='confirmar_compra'),
    path('productos/recibos/cancelar/<str:recibo_codigo>/', views.cancelar_compra, name='cancelar_compra'),
    path('vendidos/', views.report_vendidos, name='vendidos'),
    path('asignations/', views.users_asignation, name='asignations'),
    path('user_asignation/<int:id>/', views.user_asignation, name='user_asignation'),
    path('user_designation/<int:id>/', views.user_designation, name='user_designation'),

]
