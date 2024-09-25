from django.shortcuts import render, redirect, get_object_or_404
from audioyvideo.models import audioyvideo, categoria_audioyvideo
from carrito.models import Carrito, CarritoItem, Vendidos
from django.contrib import messages
from django.core.paginator import Paginator

def agregar_carrito(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(audioyvideo, id=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        cantidad = int(request.POST.get('cantidad', 1))

        if producto.quantity < cantidad:

            messages.error(request, 'No hay suficiente stock disponible para este producto.')
            return redirect('carrito', producto_id=producto.id)


        item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto_audioyvideo=producto)
        if not item_created:
            item.cantidad += cantidad 
        else:
            item.cantidad = cantidad  

        item.save()

        producto.quantity -= cantidad
        producto.save()

        carrito.total = carrito.calcular_total()
        carrito.save()

        return redirect('carrito')
    else:
        return redirect('login')

def eliminar_del_carrito_audioyvideo(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(audioyvideo, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, producto_audioyvideo=producto)


        producto.quantity += item.cantidad
        producto.save()

        item.delete()

        carrito.total = carrito.calcular_total()
        carrito.save()

        return redirect('carrito')
    else:
        return redirect('login')


def actualizar_carrito(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(audioyvideo, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, producto_audioyvideo=producto)

        nueva_cantidad = int(request.POST.get('cantidad', 1))

        if nueva_cantidad > producto.quantity:
            messages.error(request, 'No hay suficiente stock disponible para este producto.')
            return redirect('carrito')

        producto.quantity += item.cantidad  
        producto.quantity -= nueva_cantidad  
        producto.save()

        item.cantidad = nueva_cantidad
        item.save()

        carrito.total = carrito.calcular_total()
        carrito.save()

        return redirect('carrito')
    else:
        return redirect('login')


def mostrar_audioyvideo(request):
    productos_audioyvideo = audioyvideo.objects.all().order_by('created')
    categorias = categoria_audioyvideo.objects.all()

    paginator = Paginator(productos_audioyvideo, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'audioyvideo/audiouvideo.html', {
        'page_obj': page_obj, 
        'categorias': categorias,
    })

def filtro_audioyvideo(request, categoria_id=None):
    categorias = categoria_audioyvideo.objects.all() 
    productos_audioyvideo = audioyvideo.objects.all().filter(category_id=categoria_id)

    if categoria_id:
        productos = audioyvideo.objects.filter(category_id=categoria_id)  # Filtrar por la categoría seleccionada
        paginator = Paginator(productos_audioyvideo, 6)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        productos = audioyvideo.objects.all()  # Mostrar todos los productos si no hay categoría seleccionada

    return render(request, 'audioyvideo/audiouvideo.html', {
        'page_obj': page_obj, 
        'categorias': categorias,  # Pasar las categorías al template
        'productos_audioyvideo': productos,  # Pasar los productos filtrados
    })


def detail_product(request, producto_id):
    producto = get_object_or_404(audioyvideo, id=producto_id)
    producto.views += 1
    producto.save()
    
    return render(request, 'audioyvideo/product_details.html', {
        'producto': producto,
    })



