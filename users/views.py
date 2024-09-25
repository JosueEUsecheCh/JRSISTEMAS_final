from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm, UserLoginForm,CodigoVerificacionForm
from django.contrib import messages
from django.core.mail import send_mail
from .models import User_register
from django.contrib.auth import get_user_model


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # El usuario no está activo hasta que verifique el correo
            user.save()

            # Enviar el correo electrónico con el código de verificación
            send_mail(
                'Verificación de cuenta',
                f'Tu código de verificación es: {user.verification_code}',
                'noreply@example.com',  # Cambia esto por tu dirección de correo
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Te hemos enviado un correo con tu código de verificación.')
            return redirect('verificar_codigo')  # Redirige a la vista para ingresar el código
    else:
        form = UserRegisterForm()
    return render(request, 'registration/user_register.html', {'form': form})


User = get_user_model()

def verificar_codigo(request):
    if request.method == 'POST':
        form = CodigoVerificacionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            verification_code = form.cleaned_data.get('verification_code')
            try:
                user = User.objects.get(email=email)

                if user.verification_code == verification_code:
                    user.is_verified = True
                    user.is_active = True  # Activamos al usuario
                    user.save()
                    messages.success(request, 'Tu cuenta ha sido verificada exitosamente.')
                    return redirect('login')
                else:
                    messages.error(request, 'El código de verificación es incorrecto.')
            except User.DoesNotExist:
                messages.error(request, 'No se encontró ningún usuario con ese correo electrónico.')
    else:
        form = CodigoVerificacionForm()
    return render(request, 'registration/verify_email.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            

            user = authenticate(request, username=email, password=password)
            
            # Verificar el resultado de la autenticación
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Usuario o contraseña incorrecta.')
                return redirect('login')
        else:
            messages.error(request, 'Formulario no válido.')
    else:
        form = UserLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


def exit(request):
    logout(request)
    print(f"Usuario autenticado después de logout: {request.user.is_authenticated}")
    return redirect('index')


def profile(request):
    return render (request, 'profile/profile.html')