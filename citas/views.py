from datetime import date, time
from django.shortcuts import render
from .models import Cliente, Servicio, Barbero, Cita

def inicio(request):
    mensaje = ""
    tipo_mensaje = ""

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        servicio_id = request.POST.get("servicio", "").strip()
        barbero_id = request.POST.get("barbero", "").strip()
        fecha_texto = request.POST.get("fecha", "").strip()
        hora_texto = request.POST.get("hora", "").strip()

        if not all([
            nombre, telefono, servicio_id,
            barbero_id, fecha_texto, hora_texto
        ]):
            mensaje = "Completa todos los campos."
            tipo_mensaje = "error"

        elif len(nombre) > 120 or len(telefono) > 20:
            mensaje = "Revisa el nombre y el teléfono."
            tipo_mensaje = "error"

        else:
            try:
                fecha_cita = date.fromisoformat(fecha_texto)
                hora_cita = time.fromisoformat(hora_texto)

                servicio = Servicio.objects.filter(
                    pk=int(servicio_id),
                    activo=True
                ).first()

                barbero = Barbero.objects.filter(
                    pk=int(barbero_id),
                    activo=True
                ).exclude(nombre="Por asignar").first()

                if fecha_cita < date.today():
                    mensaje = "No puedes reservar una fecha pasada."
                    tipo_mensaje = "error"

                elif servicio is None or barbero is None:
                    mensaje = "Selecciona un servicio y un barbero válidos."
                    tipo_mensaje = "error"

                else:
                    cliente, creado = Cliente.objects.get_or_create(
                        telefono=telefono,
                        defaults={"nombre": nombre}
                    )

                    if not creado and cliente.nombre != nombre:
                        cliente.nombre = nombre
                        cliente.save(update_fields=["nombre"])

                    Cita.objects.create(
                        cliente=cliente,
                        barbero=barbero,
                        servicio=servicio,
                        fecha=fecha_cita,
                        hora=hora_cita
                    )

                    mensaje = (
                        "¡Cita registrada correctamente! "
                        "Tus datos se guardaron."
                    )
                    tipo_mensaje = "exito"

            except (ValueError, TypeError):
                mensaje = "La fecha, hora o selección no es válida."
                tipo_mensaje = "error"

    return render(request, "inicio.html", {
        "mensaje": mensaje,
        "tipo_mensaje": tipo_mensaje,
        "barberos": Barbero.objects.filter(activo=True).exclude(
            nombre="Por asignar"
        ),
        "servicios": Servicio.objects.filter(activo=True),
    })

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import RegistroForm


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("inicio")
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "iniciar_sesion.html",
        {"form": form},
    )


def registro(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("inicio")
    else:
        form = RegistroForm()

    return render(
        request,
        "registro.html",
        {"form": form},
    )


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")
