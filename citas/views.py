
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cita
from .form import CitaForm,LoginForm, PasswordResetRequestForm,UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm    
from django.contrib.auth import login
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotAllowed
import time
def custom_logout(request):
    logout(request)
    return redirect('login') 


def csrf_failure(request, reason=""):
    # Cerrar la sesión del usuario
    logout(request)
    # Redirigir al usuario a la página de inicio de sesión
    return redirect('login')  # Ajusta la URL de inicio de sesión según tu configuración

@login_required
def update_cita(request, cita_id):
    try:
        # Obtener la cita usando 'numero_cita'
        cita = Cita.objects.get(numero_cita=cita_id)
        print("\n ++++++",cita)
        
        if request.method == 'POST':
            # Actualizar los valores de la cita
            print("\n <>>>>>>>>>>>>><++++++<<<<<<<<<<<",request.PATCH)
            tipo_cita = request.POST.get('tipo_cita', cita.tipo_cita)
            fecha_hora_str = request.POST.get('fecha_hora', '')
            print("\n ++++++<<<<<<<<<<<",fecha_hora_str)
            print("\n ++++++<<<<<<<<<<<++++++~~~~~~~",tipo_cita)
            
            # Asegurarse de que la fecha esté en el formato correcto
            if fecha_hora_str:
                try:
                    # Convertir la fecha a formato datetime
                    cita.fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    print("Formato de fecha incorrecto")
                    # Manejar el error si el formato de fecha es incorrecto
                    pass
            
            # Actualizar el campo 'tipo_cita' y guardar
            cita.tipo_cita = tipo_cita
            cita.save()

            # Redirigir a la lista de citas
            return redirect('lista_citas')

    except Cita.DoesNotExist:
        # Si no se encuentra la cita, puedes manejar el error aquí
        print(f"Cita con id {cita_id} no encontrada")

    except Exception as e:
        # Manejar cualquier otro error
        print(e)
    # Redirigir a la lista de citas si algo falla
    return redirect('lista_citas')

@login_required
def index(request):
    print("Usuario autenticado:", request.user.is_authenticated)
    if not request.user.is_authenticated:
        print("Usuario no autenticado", request.user.is_authenticated)
        # Si la sesión ha caducado, redirige al login
        logout(request)  # Eliminar la sesión del usuario
        return redirect('login')  # Redirigir al inicio de sesión
    
    return render(request, 'index.html')

@login_required
def lista_citas(request):
    citas = Cita.objects.filter(eliminado=False)
    print("Citas visibles:", citas)

    ultima_cita = Cita.objects.last()  # Obtiene la última cita
    if ultima_cita:
        nuevo_numero_cita = ultima_cita.numero_cita + 1  # Sumar 1 al último numero_cita
    else:
        nuevo_numero_cita = 1  # Si no hay citas, iniciar con 1

    if request.method == 'POST':
        # Verificar si ya existe una cita con los mismos detalles
        tipo_cita = request.POST.get('tipo_cita')
        fecha_hora = request.POST.get('fecha_hora')
        paciente = request.POST.get('paciente')
        medico = request.POST.get('medico')

        # Buscar si ya existe una cita con los mismos detalles
        if not Cita.objects.filter(fecha_hora=fecha_hora, paciente=paciente, tipo_cita=tipo_cita).exists():
            # Si no existe, se crea la cita
            cita = Cita(tipo_cita=tipo_cita, fecha_hora=fecha_hora, paciente=paciente, medico=medico)
            cita.save()
        else:
            # Si ya existe, puedes dar un mensaje de advertencia o manejar el caso como prefieras
            messages.warning(request, 'Ya existe una cita con estos datos.')
        return redirect('lista_citas')

    return render(request, 'lista.html', {'citas': citas,'nuevo_numero_cita': nuevo_numero_cita})

def delete_cita(request, cita_id):
    if request.method == "POST":
        cita = get_object_or_404(Cita, numero_cita=cita_id)
        print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Usuario pre eliminado"," ### ",cita)
        time.sleep(500)
        usuario_pre_eliminado= cita_id
        print("Usuario pre eliminado",usuario_pre_eliminado," ### ",cita)

        cita.eliminado = True  # Suponiendo que 'estado' es un BooleanField
        cita.save()
        return redirect('lista_citas')  # Redirige a la lista después de actualizar el estado
    return HttpResponseNotAllowed(['POST'])

@login_required
def detalle_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    return render(request, 'detalle.html', {'cita': cita})

@login_required
def crear_cita(request):
    if request.method == 'POST':
        # Convertimos la fecha correctamente usando parse_datetime
        fecha_hora = parse_datetime(request.POST['fecha_hora'])
        # Obtener el último numero_cita y sumarle 1

        # Obtenemos el tipo de cita y el médico del formulario
        tipo_cita = request.POST['tipo_cita']
        medico = request.POST['medico']
        
        # Asignamos el paciente con el nombre del usuario autenticado
        paciente = request.user.get_full_name() or request.user.username

        print(fecha_hora, tipo_cita, medico, paciente)

        # Creamos y guardamos la nueva cita usando .save() con los atributos directamente
        cita = Cita(
            fecha_hora=fecha_hora,
            tipo_cita=tipo_cita,
            medico=medico,
            paciente=paciente,
            eliminado=False

        )
        
        # Guardamos la cita en la base de datos
        cita.save()

        # Redirigimos a la lista de citas
        return redirect('lista_citas')
    else:
        # En el caso de un GET, solo mostramos el formulario vacío
        return render(request, 'formulario.html')
    
def login_s(request):
    if request.method == 'POST':
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Autenticar al usuario
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # Si las credenciales son correctas, iniciar sesión
                    auth_login(request, user)
                    return redirect('index')  # Redirige a la página de inicio (ajusta según tu URL)
                else:
                    form.add_error(None, 'Credenciales inválidas')  # Agregar error en caso de que el usuario no exista
        except Exception as e:

            print(e)
    else:
        try:
            form = LoginForm()
        except Exception as e:
            print(e)
        form = LoginForm()
    try:
        return render(request, 'login.html', {'form': form})
    except Exception as e:
        print(e)
        return render(request, 'login.html', {'form': form})
    


def password_reset_request(request):
    if request.method == "POST":
        try:
            form = PasswordResetRequestForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                # Verificar si el correo está asociado a un usuario
                if User.objects.filter(email=email).exists():
                    # Si existe el usuario, enviar el correo de recuperación
                    send_mail(
                        'Recuperación de contraseña',
                        'Haz clic en el siguiente enlace para restablecer tu contraseña.',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Revisa tu correo para restablecer la contraseña.')
                    return redirect('login')
                else:
                    messages.error(request, 'El correo no está registrado en el sistema.')
        except Exception as e:
            print(e)
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})


def register(request):
    if request.method == 'POST':
        try:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                
                # Crear el nuevo usuario
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
                return redirect('login')
        except Exception as e:
            print(e)
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})