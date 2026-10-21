
from django.db import models
from decimal import Decimal

class Alquiler(models.Model):
    class Estado(models.TextChoices):
        RESERVADO = "RES", "Reservado"
        ACTIVO = "ACT", "Activo"
        FINALIZADO = "FIN", "Finalizado"
        CANCELADO = "CAN", "Cancelado"

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="alquileres"
    )

    vehiculo = models.ForeignKey(
        "flota.Vehiculo",
        on_delete=models.PROTECT,
        related_name="alquileres"
    )

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(
        max_length=3,
        choices=Estado.choices,
        default=Estado.RESERVADO
    )

    def __str__(self):
        
        return f"Alquiler {self.id} - {self.cliente}"

    # Los dias se cuentan inclusivo (recoger y devolver el mismo dia = 1 dia)
    @property
    def dias(self):
        return (self.fecha_fin - self.fecha_inicio).days + 1

    @property
    def total_vehiculo(self):
        return self.dias * self.vehiculo.categoria.tarifa_diaria

    @property
    def total_accesorios(self):
        return sum(
            (a.cantidad * a.accesorio.precio_dia * self.dias
             for a in self.accesorios_alquilados.all()),
            Decimal("0"),
        )

    @property
    def total(self):
        return self.total_vehiculo + self.total_accesorios
    
class AlquilerAccesorio(models.Model):
    alquiler = models.ForeignKey(
        Alquiler,
        on_delete=models.CASCADE,
        related_name="accesorios_alquilados"
    )

    accesorio = models.ForeignKey(
        "accesorios.Accesorio",
        on_delete=models.PROTECT,
        related_name="alquileres"
    )

    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["alquiler", "accesorio"],
                name="unique_alquiler_accesorio"
            )
        ]

    def __str__(self):
        return f"{self.accesorio} x {self.cantidad}"
