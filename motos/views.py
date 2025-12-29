from django.shortcuts import render, redirect, get_object_or_404
from urllib import request #import request module
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Moto
from .forms import MotoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Max, Min, Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
import json




def home(request):
    return render(request, 'home.html')


def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {'form': UserCreationForm})# aqui colocamos el diccionario para crear el 
        #formulario
    else:
        if request.POST['password1'] == request.POST['password2']: 
            #register user 
            try: 
                user= User.objects.create_user(username= request.POST['username'],#obtiene el usuario del formulario
                password=request.POST['password1']) #obtiene la contraseña del formulario
                user.save()
                login(request, user)#guarda una cookie en el navegador 
                return redirect('motos') #redirige a una pagina con redirect(pagina)
            except IntegrityError:
                return render(request,'singup.html', {'form':UserCreationForm, "error": 'username already exist'})
        else:
            return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'Password do not match'})
        

def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {'form': AuthenticationForm})
    else:
        authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if authenticated_user is None:
            return render(request, 'singin.html', {'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
        else:
            login(request, authenticated_user)
            return redirect('motos')

def singout(request):
     logout(request)
     return redirect('home')


#def moto_details(request, moto_id):
    #return HttpResponse(f"Details of motorcycle with ID: {moto_id}")

@login_required
def register_motorcycle(request):
    if request.method == 'GET':
        return render(request, 'registrar_moto.html', {'form': MotoForm})
    else:
        try:
            form = MotoForm(request.POST)
            new_moto = form.save(commit=False)
            new_moto.usuario = request.user
            new_moto.save()
            return redirect('motos')
        except ValueError:
            return render(request, 'registrar_moto.html', 
            {'form': MotoForm, 
            'error': 'Error al registrar la moto. Por favor, intente de nuevo.'})
        except IntegrityError:
            return render(request,'registrar_moto.html', {'form':MotoForm, "error": 'La placa ya existe. Por favor, ingrese una placa diferente.'})
        
@login_required
def view_motorcycles(request):
    moto = Moto.objects.filter(usuario=request.user)#filtra las motos por el usuario que esta logeado
    return render(request, 'motos.html', {'motos': moto})

@login_required
def edit_motorcycle(request, moto_id):
    if request.method == 'POST':
        moto = get_object_or_404(Moto, pk=moto_id, usuario=request.user)

        form = MotoForm(request.POST, instance=moto)
        return render(request, 'editar_moto.html', {'form': form, 'moto': moto})
    else:
        try:
            moto = get_object_or_404(Moto, pk=moto_id, usuario=request.user)
            form = MotoForm(request.POST, instance=moto)
            form.save()
            return redirect('motos')
        except ValueError:
            return render(request, 'editar_moto.html', 
            {'form': MotoForm, 
            'error': 'Error al editar la moto. Por favor, intente de nuevo.'})
        except IntegrityError:
            return render(request, 'editar_moto.html', 
            {'form': MotoForm, 
            'error': 'Error al editar la moto. Por favor, intente de nuevo.'})
        
@login_required
def delete_motorcycle(request, motorcycle_id):
    moto = get_object_or_404(Moto, pk=motorcycle_id, usuario=request.user)
    moto.delete()
    if request.method == 'POST':
        moto.delete()
    return redirect('motos')



@login_required
def estadisticas(request):
    # Obtener todas las motos del usuario
    motos = Moto.objects.filter(usuario=request.user)
    
    # Estadísticas básicas
    total_motos = motos.count()
    
    # Por marca
    motos_por_marca = motos.values('marca').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Por color
    motos_por_color = motos.values('color').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Por año
    motos_por_year = motos.values('year').annotate(
        total=Count('id')
    ).order_by('year')
    
    # Estadísticas numéricas
    if motos.exists():
        año_mas_nuevo = motos.aggregate(Max('year'))['year__max']
        año_mas_viejo = motos.aggregate(Min('year'))['year__min']
        año_promedio = motos.aggregate(Avg('year'))['year__avg']
        
        # Calcular antigüedad
        año_actual = datetime.now().year
        antiguedad_promedio = año_actual - (año_promedio or año_actual)
    else:
        año_mas_nuevo = año_mas_viejo = año_promedio = antiguedad_promedio = 0
    
    # Preparar datos para gráficos
    datos_grafico_marca = {
        'labels': [item['marca'] for item in motos_por_marca],
        'data': [item['total'] for item in motos_por_marca],
        'colores': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
    }
    
    datos_grafico_year = {
        'labels': [str(item['year']) for item in motos_por_year],
        'data': [item['total'] for item in motos_por_year]
    }
    
    context = {
        'total_motos': total_motos,
        'motos_por_marca': motos_por_marca,
        'motos_por_color': motos_por_color,
        'motos_por_year': motos_por_year,
        'año_mas_nuevo': año_mas_nuevo,
        'año_mas_viejo': año_mas_viejo,
        'año_promedio': round(año_promedio, 1) if año_promedio else 0,
        'antiguedad_promedio': round(antiguedad_promedio, 1),
        'datos_grafico_marca': json.dumps(datos_grafico_marca),
        'datos_grafico_year': json.dumps(datos_grafico_year),
    }
    
    return render(request, 'estadisticas.html', context)