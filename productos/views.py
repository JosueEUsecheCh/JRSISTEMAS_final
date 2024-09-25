from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import paginator
from .forms import register_products
from audioyvideo.models import categoria_audioyvideo, audioyvideo
from componentes.models import categoria_Componentes, componentes
from equipos.models import categoria_equipos, equipos
from redes.models import categoria_redes, redes
from .utils import render_report
from carrito.models import Recibo,Vendidos
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from users.models import User_register
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = register_products(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            details = form.cleaned_data['details']
            image = form.cleaned_data['image']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            category_data = form.cleaned_data['category']
            
            try:
                prefix, category_id = category_data.split('_')
                category_id = int(category_id)
                
                if prefix == 'audio':
                    categoria = categoria_audioyvideo.objects.get(id=category_id)
                    componente = audioyvideo(name=name, details=details, image=image, price=price, category=categoria, quantity=quantity)
                    componente.save()
                
                elif prefix == 'equipo':
                    categoria = categoria_equipos.objects.get(id=category_id)
                    componente_equipo = equipos(name=name, details=details, image=image, price=price, category=categoria, quantity=quantity)
                    componente_equipo.save()
                    
                elif prefix == 'componente':
                    categoria = categoria_Componentes.objects.get(id=category_id)
                    componente_componente = componentes(name=name, details=details, image=image, price=price, category=categoria, quantity=quantity)
                    componente_componente.save()

                elif prefix == 'redes':
                    categoria = categoria_redes.objects.get(id=category_id)
                    componente_componente = redes(name=name, details=details, image=image, price=price, category=categoria, quantity=quantity)
                    componente_componente.save()
                
                else:
                    return render(request, 'error.html', {'message': 'Categoría no encontrada'})
                
                return redirect('register')  # Ajusta el nombre de la URL de éxito según tu configuración
            
            except ValueError:
                return render(request, 'error.html', {'message': 'Error en la selección de categoría'})
    
    else:
        form = register_products()
    
    return render(request, 'productos/register_products.html', {'form': form})


def delete_products(request, id):
    producto = None
    modelos = [audioyvideo, componentes, equipos, redes]

    for modelo in modelos:
        try:
            producto = get_object_or_404(modelo, id=id)
            break
        except:
            continue
    if producto and request.method == 'POST':
        producto.delete()
        return redirect('panel')  

    return render(request, 'productos/panel_admin.html', {'error': 'Producto no encontrado'})

def get_prefix_from_category(category):
    if isinstance(category, categoria_audioyvideo):
        return 'audio'
    elif isinstance(category, categoria_equipos):
        return 'equipo'
    elif isinstance(category, categoria_Componentes):
        return 'componente'
    elif isinstance(category, categoria_redes):
        return 'redes'
    return ''


@staff_member_required
def panel_admin(request):
    items = []
    categorias_seleccionadas = []

    # Obtener las categorías directamente desde los modelos
    categorias_audio_video = categoria_audioyvideo.objects.all()
    categorias_equipos = categoria_equipos.objects.all()
    categorias_componentes = categoria_Componentes.objects.all()
    categorias_redes = categoria_redes.objects.all()

    # Manejar solicitudes GET
    if request.method == 'GET':
        selected_categories = request.GET.getlist('selected_categories')

        for selected in selected_categories:
            category_type, category_id = selected.split('_')

            if category_id == 'all':
                if category_type == 'audio':
                    items.extend(audioyvideo.objects.all())
                    categorias_seleccionadas.append('Audio y Video')
                elif category_type == 'equipo':
                    items.extend(equipos.objects.all())
                    categorias_seleccionadas.append('Equipos')
                elif category_type == 'componente':
                    items.extend(componentes.objects.all())
                    categorias_seleccionadas.append('Componentes')
                elif category_type == 'redes':
                    items.extend(redes.objects.all())
                    categorias_seleccionadas.append('Redes')
            else:
                if category_type == 'audio':
                    items.extend(audioyvideo.objects.filter(category_id=category_id))
                    categorias_seleccionadas.append('Audio y Video')
                elif category_type == 'equipo':
                    items.extend(equipos.objects.filter(category_id=category_id))
                    categorias_seleccionadas.append('Equipos')
                elif category_type == 'componente':
                    items.extend(componentes.objects.filter(category_id=category_id))
                    categorias_seleccionadas.append('Componentes')
                elif category_type == 'redes':
                    items.extend(redes.objects.filter(category_id=category_id))
                    categorias_seleccionadas.append('Redes')

        # Asigna el prefijo a cada item
        for item in items:
            item.prefix = get_prefix_from_category(item.category)
    print(len(items))
    # Paginación
    paginator = Paginator(items, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    return render(request, 'productos/panel_admin.html', {
        'categorias_audio_video': categorias_audio_video,
        'categorias_equipos': categorias_equipos,
        'categorias_componentes': categorias_componentes,
        'categorias_redes': categorias_redes,
        'categoria_seleccionada': ', '.join(categorias_seleccionadas),
        'page_obj': page_obj,  # Pasamos page_obj al template para iterar los ítems paginados
    })


def update_products(request, prefix, id):
    modelos = {
        "audio": audioyvideo,
        "componente": componentes,
        "equipo": equipos,
        "redes": redes
    }

    if request.method == 'POST':
        form = register_products(request.POST, request.FILES)
        if form.is_valid():
            category_str = form.cleaned_data['category']
            try:
                prefix, category_id = category_str.split('_')
                category_id = int(category_id)
                
                # Verificar el prefijo para obtener el modelo correcto
                if prefix in modelos:
                    producto_model = modelos[prefix]
                    producto = producto_model.objects.get(id=id)
                else:
                    return render(request, 'error.html', {'message': 'Categoría no encontrada'})

                # Obtener la categoría correcta según el prefijo
                if prefix == "audio":
                    categoria = get_object_or_404(categoria_audioyvideo, id=category_id)
                elif prefix == "equipo":
                    categoria = get_object_or_404(categoria_equipos, id=category_id)
                elif prefix == "componente":
                    categoria = get_object_or_404(categoria_Componentes, id=category_id)
                elif prefix == "redes":
                    categoria = get_object_or_404(categoria_redes, id=category_id)
                else:
                    return render(request, 'error.html', {'message': 'Categoría no encontrada'})

                # Actualizar los datos del producto
                producto.category = categoria
                producto.name = form.cleaned_data['name']
                producto.details = form.cleaned_data['details']
                if 'image' in request.FILES:
                    producto.image = request.FILES['image']
                producto.price = form.cleaned_data['price']
                producto.quantity = form.cleaned_data['quantity']
                producto.save()

                return redirect('panel')

            except producto_model.DoesNotExist:
                return render(request, 'error.html', {'message': 'Producto no encontrado'})
            except ValueError:
                return render(request, 'error.html', {'message': 'Error en la selección de categoría'})
        else:
            return render(request, 'productos/update_products.html', {'form': form, 'error': 'Error al actualizar el producto'})

    else:
        # Obtener el modelo correcto antes de cargar el formulario inicial
        if prefix in modelos:
            producto_model = modelos[prefix]
            try:
                producto = producto_model.objects.get(id=id)
            except producto_model.DoesNotExist:
                return render(request, 'error.html', {'message': 'Producto no encontrado'})
            
            image = producto.image

            form = register_products(initial={
                'name': producto.name,
                'details': producto.details,
                'image': producto.image,
                'price': producto.price,
                'quantity': producto.quantity,
                'category': producto.category,
            })
        else:
            return render(request, 'error.html', {'message': 'Modelo no encontrado'})

    return render(request, 'productos/update_products.html', {'form': form, 'image': producto.image.url, 'name':producto.name})



def reports_pdf(request):
    if request.method == 'GET':
        Redes = redes.objects.all().order_by('name')
        AudioVideo = audioyvideo.objects.all().order_by('name')
        Equipos = equipos.objects.all().order_by('name')
        Componentes= componentes.objects.all().order_by('name')
        data = {'productos_audioyvideo': AudioVideo, 'productos_redes': Redes, 'productos_equipo': Equipos, 'productos_componentes': Componentes}
        pdf = render_report('productos/reporte.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

def listar_recibos(request):
    # Obtén todos los códigos de recibo asociados con productos confirmados
    recibo_codigos_confirmados = Vendidos.objects.filter(producto_compra=True).values_list('producto_codigo', flat=True)

    # Filtra los recibos basados en los códigos de recibo obtenidos
    recibos = Recibo.objects.exclude(recibo_codigo__in=recibo_codigos_confirmados).order_by('-fecha_generacion')

    return render(request, 'productos/listar_recibos.html', {'recibos': recibos})


def confirmar_compra(request, recibo_codigo):
    # Obtén el recibo basado en el código proporcionado
    recibo = get_object_or_404(Recibo, recibo_codigo=recibo_codigo)
    
    try:
        # Filtra los productos vendidos relacionados con el recibo
        productos_vendidos = Vendidos.objects.filter(producto_codigo=recibo_codigo)
        
        if not productos_vendidos.exists():
            messages.error(request, 'No se encontraron productos asociados con este recibo.')
            return redirect('listar_recibos')  # Redirige a la lista de recibos

        # Lógica para confirmar la compra
        for producto in productos_vendidos:
            producto.producto_compra = True
            producto.save()

        # Envía un mensaje de éxito
        messages.success(request, '¡La compra ha sido confirmada exitosamente!')
    
    except Exception as e:
        # Si ocurre cualquier otro error, muestra un mensaje de error
        messages.error(request, f'Error al confirmar la compra: {e}')
    
    # Redirige a la vista de la lista de recibos
    return redirect('listar_recibos')  # Cambia 'lista_recibos' por el nombre de la URL correcta


def cancelar_compra(request, recibo_codigo):
    # Suponiendo que recibo_codigo es el código que también se utiliza en producto_codigo
    productos_vendidos = Vendidos.objects.filter(producto_codigo=recibo_codigo)
    
    if productos_vendidos.exists():
        # Eliminar los productos asociados al recibo
        productos_vendidos.delete()
    
    # Aquí podrías eliminar el recibo también si es necesario
    recibo = get_object_or_404(Recibo, recibo_codigo=recibo_codigo)
    recibo.delete()

    return redirect('listar_recibos')

def report_vendidos(request):
    if request.method == 'GET':
        confirmados = Vendidos.objects.filter(producto_compra=True)
        total = sum([producto.producto_price * producto.producto_quantity for producto in confirmados])
        data = {
            'confirmados': confirmados,
            'total': total
        }
        pdf = render_report('productos/vendidos.html', data)

        return HttpResponse(pdf, content_type='application/pdf')


@user_passes_test(lambda u: u.is_superuser)
def users_asignation(request):
    users = User_register.objects.all().order_by('id') 
    print(users)
    return render(request, 'productos/users_asignation.html', {'users': users })

@user_passes_test(lambda u: u.is_superuser)
def user_asignation(request, id):
    users = User_register.objects.all().order_by('id') 
    user = get_object_or_404(User_register, id=id)
    if user:
        if not user.is_staff:
            user.is_staff = True
            user.save()
            print("nyehehe") 
        else:
            print("Ya es staff")
    else:
        print("No hay usuario")
    return render(request, 'productos/users_asignation.html', {'users': users })

@user_passes_test(lambda u: u.is_superuser)
def user_designation(request, id):
    users = User_register.objects.all().order_by('id') 
    user = get_object_or_404(User_register, id=id)
    if user:
        if user.is_staff: 
            user.is_staff = False
            user.save()
            print("nyehehe") 
    else:
        print("No hay usuario")
    return render(request, 'productos/users_asignation.html', {'users': users })

""" 
def lista_productos(request):
    productos = mostrar_tablas.all()  # Obtén todos los productos
    paginator = paginator(productos, 10)  # Muestra 10 productos por página

    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtén los productos para esa página

    return render(request, 'tu_template.html', {'page_obj': page_obj})
    
"""