from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator
from gestion_tareas.models import Tarea
from django.contrib import messages
from gestion_tareas.forms import FormTarea
from django.db.models import Q

# Create your views here.

def index(request):
    # Validamos autenticacion
    if not 'usuario' in request.session:
        return redirect('login')

    # Obtenemos tareas. Devuelve tuplas. usuario, solo retorna el campo id
    # tareas = Tarea.objects.values_list('id', 'title', 'created_at', 'usuario')

    # Obtenemos tareas. Devuelve objetos. Tambien devuelve objetos relacionados
    tareas = Tarea.objects.all()

    # Obtenemos tareas con filtro de busqueda.
    cadena_buscador = ''
    if request.method == 'GET':
        if 'searchtext' in request.GET:
            searchtext = request.GET.get('searchtext').strip()
            tareas = Tarea.objects.filter( Q(usuario__first_name__contains=searchtext) | Q(usuario__last_name__contains=searchtext) ) # LIKE first_name OR LIKE last_name
            cadena_buscador = '&searchtext='+searchtext

    # Paginar los articulos
    paginator = Paginator(tareas, 5)

    # Recoger numero pagina
    page = request.GET.get('page')
    page_tareas = paginator.get_page(page)

    return render(request, 'gestion_tareas/index.html', {
        'title': 'Gestion de Tareas',
        'tareas': page_tareas,
        'cantidad_pagina': page_tareas.object_list.count,
        'cantidad_total': paginator.count,
        'cadena_buscador': cadena_buscador
    })

def create(request):
    # Validamos autenticacion
    if not 'usuario' in request.session:
        return redirect('login')

    return render(request, 'gestion_tareas/create.html', {
        'title': 'Crear Tareas',
    })

def save(request):
    # Validamos autenticacion
    if not 'usuario' in request.session:
        return redirect('login')

    # print('POST:', request.POST)
    # print(request.session['usuario'])
    # exit()

    # Recoger datos del formulario
    if request.method == "POST":
        if 'Crear' in request.POST:

            # Recoger datos del formulario
            title = request.POST['title'].strip()
            description = request.POST['description'].strip()
            delivery_at = request.POST['delivery_at']
            usuario_id = request.session['usuario'][0]

            # Validacion con Forms Django
            form = FormTarea(request.POST)
            if not form.is_valid():
                messages.warning(request, form.errors)
                return redirect('create_tarea')

            # Validacion
            # errores = {}
            # if (title == '' or title == None):
            #     errores['title'] = 'El titulo no es válido'
            # if (description == '' or description == None):
            #     errores['description'] = 'La descripcion no es válida'
            # if (delivery_at == '' or delivery_at == None):
            #     errores['delivery_at'] = 'La fecha de entrega no es válida'

            # if (len(errores) > 0):
            #     for error in errores:
            #         messages.warning(request, errores[error])
            #     return redirect('create_tarea')

            # Obtenemos datos
            tarea = Tarea(
                title = title,
                description = description,
                delivery_at = delivery_at,
                usuario_id = usuario_id
            )

            # Guardamos
            try:
                tarea.save()
                messages.success(request, 'La tarea se creo correctamente')
                return redirect('index_tareas')
            except Exception as e:
                messages.warning(request, 'ERROR: ' + str(e))
                return redirect('create_tarea')

def view(request, id):
    # Validamos autenticacion
    if not 'usuario' in request.session:
        return redirect('login')

    # Obtenemos tarea
    tarea = Tarea.objects.get(id=id)

    return render(request, 'gestion_tareas/view.html', {
        'title': 'Detalle Tarea',
        'tarea': tarea
    })

def delete(request, id):
    # Validamos autenticacion
    if not 'usuario' in request.session:
        return redirect('login')

    # Obtenemos tarea
    tarea = Tarea.objects.get(id=id)

    tarea.delete()
    messages.warning(request, 'La tarea se elimino correctamente')
    return redirect('index_tareas')
