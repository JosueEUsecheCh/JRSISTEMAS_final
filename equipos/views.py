from django.shortcuts import render, redirect, get_object_or_404
from equipos.models import equipos, categoria_equipos
from carrito.models import Carrito, CarritoItem
from django.contrib import messages
from django.core.paginator import Paginator

def agregar_carrito(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(equipos, id=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        cantidad = int(request.POST.get('cantidad', 1))  

        if producto.quantity < cantidad:
            messages.error(request, 'No hay suficiente stock disponible para este producto.')
            return redirect('carrito', producto_id=producto.id)

        item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto_equipos=producto)
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

def eliminar_del_carrito_equipos(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(equipos, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, producto_equipos=producto)

        # Devolver el stock al producto
        producto.quantity += item.cantidad
        producto.save()

        # Eliminar el item del carrito
        item.delete()

        # Recalcula el total del carrito
        carrito.total = carrito.calcular_total()
        carrito.save()

        return redirect('carrito')
    else:
        return redirect('login')


def actualizar_carrito(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(equipos, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, producto_equipos=producto)

        nueva_cantidad = int(request.POST.get('cantidad', 1))

        if nueva_cantidad > producto.quantity:
            messages.error(request, 'No hay suficiente stock disponible para este producto.')
            return redirect('carrito')

        # Actualizar stock
        producto.quantity += item.cantidad  # Restaurar la cantidad anterior al stock
        producto.quantity -= nueva_cantidad  # Restar la nueva cantidad del stock
        producto.save()

        # Actualizar el item en el carrito
        item.cantidad = nueva_cantidad
        item.save()

        # Actualizar el total del carrito
        carrito.total = carrito.calcular_total()
        carrito.save()

        return redirect('carrito')
    else:
        return redirect('login')


def mostrar_equipos(request):
    productos_equipos = equipos.objects.all().order_by('created')
    categorias = categoria_equipos.objects.all()

    paginator = Paginator(productos_equipos, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'equipos/equipos.html', {
        'page_obj': page_obj,
        'categorias':categorias,
    })

def filtro_equipos(request, categoria_id=None):
    categorias = categoria_equipos.objects.all()  # Obtener todas las categorías
    productos_equipos = equipos.objects.all().filter(category_id=categoria_id)

    if categoria_id:
        productos = equipos.objects.filter(category_id=categoria_id)  # Filtrar por la categoría seleccionada
        paginator = Paginator(productos_equipos, 6)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        productos = equipos.objects.all()  # Mostrar todos los productos si no hay categoría seleccionada

    return render(request, 'equipos/equipos.html', {
        'page_obj': page_obj,
        'categorias': categorias,  # Pasar las categorías al template
        'productos_equipos': productos,  # Pasar los productos filtrados
    })

def detail_product(request, producto_id):
    producto = get_object_or_404(equipos, id=producto_id)
    producto.views += 1
    producto.save()
    
    return render(request, 'equipos/product_details.html', {
        'producto': producto,
    })

