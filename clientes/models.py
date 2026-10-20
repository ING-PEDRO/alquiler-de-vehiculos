
from django.db import models


class Cliente(models.Model):
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
