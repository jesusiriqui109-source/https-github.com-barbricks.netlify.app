
from django.db import models


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    duracion_minutos = models.PositiveIntegerField(default=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Barbero(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="citas",
    )
    barbero = models.ForeignKey(
        Barbero,
        on_delete=models.PROTECT,
        related_name="citas",
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        related_name="citas",
    )
    fecha = models.DateField()
    hora = models.TimeField()
    notas = models.TextField(blank=True)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora"]

    def __str__(self):
        return f"{self.cliente} - {self.fecha} {self.hora}"
