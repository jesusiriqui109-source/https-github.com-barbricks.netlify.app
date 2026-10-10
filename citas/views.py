
from datetime import date, time

from django.shortcuts import render
from django.db import transaction

from .models import Cliente, Servicio, Barbero, Cita


def inicio(request):
    mensaje = ""
    tipo_mensaje = ""

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        nombre_servicio = request.POST.get("servicio", "").strip()
        nombre_barbero = request.POST.get("barbero", "").strip()
        fecha_texto = request.POST.get("fecha", "").strip()
        hora_texto = request.POST.get("hora", "").strip()

        if not all([
            nombre,
            telefono,
            nombre_servicio,
            nombre_barbero,
            fecha_texto,
            hora_texto,
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

                if fecha_cita < date.today():
                    raise ValueError

                with transaction.atomic():
                    servicio, _ = Servicio.objects.get_or_create(
                        nombre=nombre_servicio,
                        defaults={
                            "precio": 0,
                            "duracion_minutos": 30,
                            "activo": True,
                        },
                    )

                    barbero, _ = Barbero.objects.get_or_create(
                        nombre=nombre_barbero,
                        defaults={"activo": True},
                    )

                    cliente, creado = Cliente.objects.get_or_create(
                        telefono=telefono,
                        defaults={"nombre": nombre},
                    )

                    if not creado and cliente.nombre != nombre:
                        cliente.nombre = nombre
                        cliente.save(update_fields=["nombre"])

                    Cita.objects.create(
                        cliente=cliente,
                        barbero=barbero,
                        servicio=servicio,
                        fecha=fecha_cita,
                        hora=hora_cita,
                    )

                mensaje = (
                    "¡Cita registrada correctamente! "
                    "Tus datos se guardaron."
                )
                tipo_mensaje = "exito"

            except ValueError:
                mensaje = "La fecha o la hora no son válidas."
                tipo_mensaje = "error"


    return render(request, "inicio.html", {
        "mensaje": mensaje,
        "tipo_mensaje": tipo_mensaje,
        "barberos": Barbero.objects.filter(activo=True),
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
