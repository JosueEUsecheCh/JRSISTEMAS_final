from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import Carrito
from productos.utils import render_report
from django.core.mail import EmailMessage
from io import BytesIO
from django.contrib import messages
from .utils import render_report
from .models import Vendidos,Recibo

def mostrar_producto(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        items = carrito.items.all() if carrito else []

        return render(request, 'carrito/carrito.html', {
            'carrito': carrito,
            'items': items,
        })
    else:
        return redirect('login')

def reports_pdf(request):
    if request.method == 'GET':
        carrito = Carrito.objects.filter(usuario=request.user).first()
        items = carrito.items.all().order_by('id') if carrito else []
        data = {'carrito': carrito, 'items': items}
        try:
            pdf = render_report('carrito/recibo.html', data)  
            return HttpResponse(pdf, content_type='application/pdf')
        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            return HttpResponse(status=500)
        
    return HttpResponse(status=405)

def recibo_correo(request):
    if request.method == 'POST':
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if not carrito:
            messages.error(request, 'No hay productos en el carrito.')
            return redirect('carrito')

        recibo = Recibo.objects.create(carrito=carrito, usuario=request.user)
        
        data = {
            'carrito': carrito,
            'items': carrito.items.all().order_by('id'),
            'recibo_code': recibo.recibo_codigo  # Agrega el código del recibo a los datos
        }
        
        pdf_response = render_report('carrito/recibo.html', data)
        pdf_file = BytesIO(pdf_response.content)

        email = EmailMessage(
            subject='Tu recibo de compra',
            body=f'Tu recibo de compra con el código {recibo.recibo_codigo} está adjunto.',
            from_email='jrsistemas57@gmail.com',
            to=[request.user.email]
        )
        email.attach('recibo.pdf', pdf_file.read(), 'application/pdf')
        email.send()

        vendidos = []
        for item in carrito.items.all():
            if item.producto_audioyvideo:
                vendidos.append(Vendidos(
                    producto_name=item.producto_audioyvideo.name,
                    producto_price=item.producto_audioyvideo.price,
                    producto_quantity=item.cantidad,
                    producto_state=True,
                    producto_codigo=recibo.recibo_codigo  
                ))
            elif item.producto_componentes:
                vendidos.append(Vendidos(
                    producto_name=item.producto_componentes.name,
                    producto_price=item.producto_componentes.price,
                    producto_quantity=item.cantidad,
                    producto_state=True,
                    producto_codigo=recibo.recibo_codigo 
                ))
            elif item.producto_equipos:
                vendidos.append(Vendidos(
                    producto_name=item.producto_equipos.name,
                    producto_price=item.producto_equipos.price,
                    producto_quantity=item.cantidad,
                    producto_state=True,
                    producto_codigo=recibo.recibo_codigo  
                ))
            elif item.producto_redes:
                vendidos.append(Vendidos(
                    producto_name=item.producto_redes.name,
                    producto_price=item.producto_redes.price,
                    producto_quantity=item.cantidad,
                    producto_state=True,
                    producto_codigo=recibo.recibo_codigo  
                ))

        Vendidos.objects.bulk_create(vendidos)

        carrito.items.all().delete()
        carrito.total = 0
        carrito.save()
        messages.success(request, f'Tu recibo ha sido enviado al correo electrónico con el código {recibo.recibo_codigo}.')

        return redirect('carrito')
    else:
        return redirect('login')