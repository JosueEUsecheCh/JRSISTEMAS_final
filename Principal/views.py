from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from JRSISTEMAS import settings
from django.contrib import messages
from django.shortcuts import render
from audioyvideo.models import audioyvideo
from equipos.models import equipos
from componentes.models import componentes
from redes.models import redes

def index(request):
    # Obtén los productos de todos los modelos
    audioyvideo_products = audioyvideo.objects.all()
    equipos_products = equipos.objects.all()
    componentes_products = componentes.objects.all()
    redes_products = redes.objects.all()

    # Combina todos los productos en una sola lista
    all_products = list(audioyvideo_products) + list(equipos_products) + list(componentes_products) + list(redes_products)

    # Ordena los productos por el campo de vistas (de mayor a menor)
    all_products_sorted = sorted(all_products, key=lambda x: x.views, reverse=True)

    # Selecciona los 5 productos más vistos
    top_products = all_products_sorted[:5]

    # Añadir un campo para identificar la app
    for product in top_products:
        if isinstance(product, audioyvideo):
            product.app_label = 'audioyvideo'
        elif isinstance(product, componentes):
            product.app_label = 'componentes'
        elif isinstance(product, equipos):
            product.app_label = 'equipos'
        elif isinstance(product, redes):
            product.app_label = 'redes'

    # Renderiza la plantilla del índice con los productos más vistos
    return render(request, 'index/index.html', {'top_products': top_products})

def servicioT(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        servicio = request.POST['servicio']
        message = request.POST['message']

        # Renderizar el contenido del correo como HTML
        template = render_to_string('index/emailtemplate.html', {
            'name': name,
            'email': email,
            'servicio': servicio,
            'message': message,
        })
        
        # Enviar el correo
        emailSender = EmailMessage(
            subject=f'Nuevo servicio solicitado: {servicio}',  # Asunto del correo
            body=template,  # Contenido del correo
            from_email=settings.EMAIL_HOST_USER,  # Correo de origen
            to=['jrsistemas57@gmail.com'],  # Lista de destinatarios
        )
        emailSender.content_subtype = 'html'  # Definir que es un contenido HTML
        emailSender.fail_silently = False  # Si hay error, Django lo informará
        
        try:
            emailSender.send()
            messages.success(request, 'El correo fue enviado correctamente')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {str(e)}')

    return render(request, 'index/servicioT.html')
