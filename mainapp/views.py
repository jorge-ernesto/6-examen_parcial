from django.shortcuts import render, redirect
from mainapp.models import Usuario
from django.contrib import messages
import hashlib
from django.contrib.auth import logout

# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html', {
        'title': 'Inicio'
    })

def register_page(request):
    # Validamos autenticacion
    if 'usuario' in request.session:
        return redirect('inicio')
    else:
        # Mostramos formulario de registro
        return render(request, 'users/register.html', {
            'title': 'Registrarse'
        })

def register_action(request):
    # print('POST:', request.POST)
    # exit()

    # Recoger datos del formulario
    if request.method == "POST":
        if 'Registrarse' in request.POST:

            # Recoger datos del formulario
            username = request.POST['username'].strip()
            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()
            password1 = request.POST['password1'].strip()
            password2 = request.POST['password2'].strip()

            # Validacion
            errores = {}
            if password1 != password2:
                errores['password1'] = 'La contraseña no coincide'
            if (username == '' or username == None):
                errores['username'] = 'El usuario no es válido'
            if (first_name == '' or first_name == None):
                errores['first_name'] = 'El nombres no es válido'
            if (last_name == '' or last_name == None):
                errores['last_name'] = 'El apellido no es válido'
            if (password1 == '' or password1 == None):
                errores['password1'] = 'La contraseña no es válida'
            if (password2 == '' or password2 == None):
                errores['password2'] = 'La contraseña (confirmación) no es válida'

            if (len(errores) > 0):
                for error in errores:
                    messages.warning(request, errores[error])
                return redirect('register')

            # Cifrar contraseña
            cifrado = hashlib.sha256()
            cifrado.update(password1.encode('utf8')) # El metodo update recibe un byte
            password_cifrado = cifrado.hexdigest() # Obtenemos el string hexadecimal del cifrado que genero la libreria

            # Obtenemos datos
            usuario = Usuario(
                username = username,
                first_name = first_name,
                last_name = last_name,
                password = password_cifrado
            )

            # Guardamos
            try:
                usuario.save()
                messages.success(request, 'El usuario se creo correctamente')
                return redirect('login')
            except Exception as e:
                messages.warning(request, 'ERROR: ' + str(e))
                return redirect('register')

def login_page(request):
    # Validamos autenticacion
    if 'usuario' in request.session:
        return redirect('inicio')
    else:
        # Mostramos formulario de login
        return render(request, 'users/login.html', {
            'title': 'Login'
        })

def login_action(request):
    # print('POST:', request.POST)
    # exit()

    # Recoger datos del formulario
    if request.method == "POST":
        if 'Login' in request.POST:

            # Recoger datos del formulario
            username = request.POST['username'].strip()
            password = request.POST['password'].strip()

            # Cifrar contraseña
            cifrado = hashlib.sha256()
            cifrado.update(password.encode('utf8')) # El metodo update recibe un byte
            password_cifrado = cifrado.hexdigest() # Obtenemos el string hexadecimal del cifrado que genero la libreria

            # Consulta para comprobar credenciales del usuario
            resultado = Usuario.objects.filter(username=username).values_list('id', 'first_name', 'last_name', 'username', 'password')
            print('USUARIO:', resultado)

            # Manejo de error, validamos existencia de indice de tupla
            try:
                usuario = resultado[0]
            except Exception as e:
                messages.warning(request, 'Login incorrecto!!')
                return redirect('login')

            if usuario[4] and len(resultado) == 1:
                # Comprobar la contraseña
                if password_cifrado == usuario[4]:
                    # Utilizar una sesión para guardar los datos del usuario logueado
                    request.session['usuario'] = usuario
                else:
                    # Si algo falla enviar una sesión con el fallo
                    messages.warning(request, 'Login incorrecto!!')
                    return redirect('login')
            else:
                # mensaje de error
                messages.warning(request, 'Login incorrecto2!!')
                return redirect('login')

            # Redirigir al inicio
            return redirect('inicio')

def logout_user(request):
    logout(request)
    return redirect('login')
