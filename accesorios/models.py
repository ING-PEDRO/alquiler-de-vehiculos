from django.db import models


class Accesorio(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    precio_dia = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre