
from django.contrib import admin
from .models import Cita, Cliente, Barbero, Servicio


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "barbero", "servicio", "fecha", "hora")
    list_filter = ("fecha", "barbero", "servicio")
    search_fields = ("cliente__nombre", "cliente__telefono")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "telefono")
    search_fields = ("nombre", "telefono")


@admin.register(Barbero)
class BarberoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especialidad", "activo")
    list_filter = ("activo",)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "duracion_minutos", "activo")
    list_filter = ("activo",)
