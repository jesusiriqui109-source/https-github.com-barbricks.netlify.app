
from django.contrib import admin
from django.urls import path
from citas import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.inicio, name="inicio"),
    path(
        "iniciar-sesion/",
        views.iniciar_sesion,
        name="iniciar_sesion",
    ),
    path(
        "registro/",
        views.registro,
        name="registro",
    ),
    path(
        "cerrar-sesion/",
        views.cerrar_sesion,
        name="cerrar_sesion",
    ),
]
