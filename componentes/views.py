from django.shortcuts import render, redirect, get_object_or_404
from componentes.models import componentes, categoria_Componentes
from carrito.models import Carrito, CarritoItem
from django.contrib import messages
from django.core.paginator import Paginator

def agregar_carrito(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(componentes, id=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        cantidad = int(request.POST.get('cantidad', 1))  

        if producto.quantity < cantidad:

            messages.error(request, 'No hay suficiente stock disponible para este producto.')
            return redirect('carrito', producto_id=producto.id)

        item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto_componentes=producto)
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

def eliminar_del_carrito_componentes(request, producto_id):
    if request.user.is_authenticated:
        producto = get_object_or_404(componentes, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, producto_componentes=producto)

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
        producto = get_object_or_404(componentes, id=producto_id)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(CarritoItem, carrito=carrito, producto_componentes=producto)

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

def detail_product(request, producto_id):
    producto = get_object_or_404(componentes, id=producto_id)
    producto.views += 1
    producto.save()
    
    return render(request, 'componentes/product_details.html', {
        'producto': producto,
    })

def mostrar_componentes(request):
    productos_componentes = componentes.objects.all().order_by('created')
    categorias = categoria_Componentes.objects.all() 

    paginator = Paginator(productos_componentes, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'componentes/componentes.html', {
        'page_obj': page_obj,
        'categorias': categorias,
    })

def filtro_componentes(request, categoria_id=None):
    categorias = categoria_Componentes.objects.all()  # Obtener todas las categorías
    productos_componentes = componentes.objects.all().filter(category_id=categoria_id)
    if categoria_id:
        productos = componentes.objects.filter(category_id=categoria_id)  # Filtrar por la categoría seleccionada
        paginator = Paginator(productos_componentes, 6)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        productos = componentes.objects.all()  # Mostrar todos los productos si no hay categoría seleccionada

    return render(request, 'componentes/componentes.html', {
        'page_obj': page_obj,
        'categorias': categorias,  # Pasar las categorías al template
        'productos_componentes': productos,  # Pasar los productos filtrados
    })
