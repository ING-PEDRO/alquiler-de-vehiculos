
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)
    tarifa_diaria = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = "DISP", "Disponible"
        ALQUILADO = "ALQ", "Alquilado"
        MANTENIMIENTO = "MANT", "En mantenimiento"

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="vehiculos"
    )
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=40)
    modelo = models.CharField(max_length=40)
    anio = models.PositiveSmallIntegerField()
    estado = models.CharField(
        max_length=4,
        choices=Estado.choices,
        default=Estado.DISPONIBLE
    )

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"


class Mantenimiento(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="mantenimientos"
    )
    fecha = models.DateField()
    descripcion = models.TextField()
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.fecha}"
