from django.shortcuts import render
from main.services import crear_user, editar_user_sin_password, cambio_password, crear_inmueble, editar_inmueble, eliminar_inmueble, filtro_comuna_region
from django.contrib.auth.decorators import login_required
from main.models import Inmueble, Region, Comuna
from django.contrib import messages

def index(request):
    # Recibe información vía get:
    propiedades = Inmueble.objects.all()
    datos = request.GET
    comuna_cod = datos.get('comuna_cod', '')
    region_cod = datos.get('region_cod', '')
    tipo_inmueble = datos.get('tipo_inmueble', '')

    propiedades = filtro_comuna_region(comuna_cod, region_cod, tipo_inmueble)

    comunas = Comuna.objects.all().order_by('nombre')
    regiones = Region.objects.all()
    tipos_inmuebles = Inmueble.inmuebles
    context = {
        'comunas': comunas,
        'regiones': regiones,
        'tipos_inmuebles': tipos_inmuebles,
        'propiedades': propiedades
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        rol = request.POST['rol']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
            
        crear = crear_user(username, first_name, last_name, email, password, password_repeat, direccion, rol, telefono)

        if crear: # Si crear es True
            messages.success(request, 'Usuario creado con éxito. Por favor ingrese.')
            return redirect('/accounts/login') 
        # Si llegó, crear fue False
        messages.warning(request, 'Por favor, revise los datos ingresados')
        return render(request, 'registration/register.html', {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'direccion': direccion,
            'telefono': telefono,
            'rol': rol,
            })
    else: # en caso de metodo GET
        return render(request, 'registration/register.html')
