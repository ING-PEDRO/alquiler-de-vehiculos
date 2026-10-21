
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from accesorios.models import Accesorio
from alquileres.models import Alquiler, AlquilerAccesorio
from clientes.models import Cliente
from config.permissions import (
    ADMINISTRADOR,
    ASESOR,
    CLIENTE,
    JEFE_FLOTA,
    ROLES,
)
from flota.models import Categoria, Vehiculo


USUARIOS = {
    "admin": (ADMINISTRADOR, True),
    "asesor": (ASESOR, False),
    "jefeflota": (JEFE_FLOTA, False),
    "cliente": (CLIENTE, False),
}


class Command(BaseCommand):
    help = "Crea roles, usuarios y datos de prueba"

    def handle(self, *args, **options):
        grupos = {
            nombre: Group.objects.get_or_create(name=nombre)[0]
            for nombre in ROLES
        }

        usuarios = {}

        for username, (rol, administrador) in USUARIOS.items():
            usuario, creado = User.objects.get_or_create(
                username=username,
                defaults={
                    "is_staff": administrador,
                    "is_superuser": administrador,
                },
            )

            if creado:
                usuario.set_password("demo1234")
                usuario.save()

            usuario.groups.add(grupos[rol])
            usuarios[username] = usuario

        economico, _ = Categoria.objects.get_or_create(
            nombre="Economico",
            defaults={"tarifa_diaria": Decimal("90000")},
        )

        suv, _ = Categoria.objects.get_or_create(
            nombre="SUV",
            defaults={"tarifa_diaria": Decimal("220000")},
        )

        Vehiculo.objects.get_or_create(
            placa="ABC123",
            defaults={
                "categoria": economico,
                "marca": "Renault",
                "modelo": "Logan",
                "anio": 2022,
            },
        )

        vehiculo_suv, _ = Vehiculo.objects.get_or_create(
            placa="DEF456",
            defaults={
                "categoria": suv,
                "marca": "Toyota",
                "modelo": "Fortuner",
                "anio": 2023,
            },
        )

        gps, _ = Accesorio.objects.get_or_create(
            nombre="GPS",
            defaults={
                "precio_dia": Decimal("15000"),
                "stock": 5,
            },
        )

        cliente, _ = Cliente.objects.get_or_create(
            numero_documento="1010101010",
            defaults={
                "tipo_documento": "CC",
                "nombres": "Ana",
                "apellidos": "Gomez",
                "telefono": "3001234567",
                "usuario": usuarios["cliente"],
            },
        )

        if not Alquiler.objects.exists():
            hoy = date.today()

            alquiler = Alquiler.objects.create(
                cliente=cliente,
                vehiculo=vehiculo_suv,
                fecha_inicio=hoy + timedelta(days=2),
                fecha_fin=hoy + timedelta(days=5),
            )

            AlquilerAccesorio.objects.create(
                alquiler=alquiler,
                accesorio=gps,
                cantidad=1,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Datos de prueba creados correctamente. Clave: demo1234"
            )
        )
