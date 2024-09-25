from django.urls import path, re_path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('user_register/', views.user_register, name='user_register' ),
    path('verificar_codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.exit, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('reset/password_reset/', PasswordResetView.as_view(
        template_name='registration/password_reset_forms.html',
        email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),
    path('reset/password_reset_done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done1.html'
    ), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm1.html'),name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete1.html'
    ), name='password_reset_complete'),
]
