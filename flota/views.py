
from datetime import date

from django.db.models import Sum
from rest_framework import serializers

from flota.models import Vehiculo
from alquileres.models import Alquiler, AlquilerAccesorio
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from config.permissions import RolePermission, ASESOR, CLIENTE, JEFE_FLOTA
from .models import Categoria, Vehiculo, Mantenimiento
from .serializers import (
    CategoriaSerializer,
    VehiculoSerializer,
    MantenimientoSerializer,
)


ESTADOS_VIGENTES = [
    Alquiler.Estado.RESERVADO,
    Alquiler.Estado.ACTIVO,
]


class AlquilerAccesorioSerializer(serializers.ModelSerializer):
    accesorio_nombre = serializers.CharField(
        source="accesorio.nombre",
        read_only=True,
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = AlquilerAccesorio
        fields = [
            "id",
            "alquiler",
            "accesorio",
            "accesorio_nombre",
            "cantidad",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return (
            obj.cantidad
            * obj.accesorio.precio_dia
            * obj.alquiler.dias
        )

    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "La cantidad debe ser al menos 1."
            )
        return value

    def validate(self, attrs):
        def obtener(campo):
            if campo in attrs:
                return attrs[campo]
            if self.instance:
                return getattr(self.instance, campo, None)
            return None

        alquiler = obtener("alquiler")
        accesorio = obtener("accesorio")
        cantidad = obtener("cantidad")

        if not alquiler or not accesorio or cantidad is None:
            raise serializers.ValidationError(
                "Debes indicar el alquiler, el accesorio y la cantidad."
            )

        if alquiler.estado not in ESTADOS_VIGENTES:
            raise serializers.ValidationError(
                "Solo se pueden gestionar accesorios de alquileres "
                "reservados o activos."
            )

        usados = (
            AlquilerAccesorio.objects.filter(
                accesorio=accesorio,
                alquiler__estado__in=ESTADOS_VIGENTES,
                alquiler__fecha_inicio__lte=alquiler.fecha_fin,
                alquiler__fecha_fin__gte=alquiler.fecha_inicio,
            )
            .exclude(pk=self.instance.pk if self.instance else None)
            .aggregate(total=Sum("cantidad"))["total"]
            or 0
        )

        disponible = accesorio.stock - usados

        if cantidad > disponible:
            raise serializers.ValidationError({
                "cantidad": (
                    f"Stock insuficiente: quedan "
                    f"{max(disponible, 0)} unidades disponibles "
                    "para esas fechas."
                )
            })

        return attrs


class AlquilerSerializer(serializers.ModelSerializer):
    estado = serializers.CharField(
        source="get_estado_display",
        read_only=True,
    )
    codigo_estado = serializers.CharField(
        source="estado",
        read_only=True,
    )
    accesorios_alquilados = AlquilerAccesorioSerializer(
        many=True,
        read_only=True,
    )
    dias = serializers.IntegerField(read_only=True)
    total_vehiculo = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )
    total_accesorios = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )
    total = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Alquiler
        fields = [
            "id",
            "cliente",
            "vehiculo",
            "fecha_inicio",
            "fecha_fin",
            "estado",
            "codigo_estado",
            "dias",
            "accesorios_alquilados",
            "total_vehiculo",
            "total_accesorios",
            "total",
        ]

    def validate(self, attrs):
        def obtener(campo):
            if campo in attrs:
                return attrs[campo]
            if self.instance:
                return getattr(self.instance, campo, None)
            return None

        inicio = obtener("fecha_inicio")
        fin = obtener("fecha_fin")
        vehiculo = obtener("vehiculo")

        if not inicio or not fin or not vehiculo:
            raise serializers.ValidationError(
                "Debes indicar el vehículo y las fechas del alquiler."
            )

        if (
            self.instance
            and self.instance.estado != Alquiler.Estado.RESERVADO
        ):
            raise serializers.ValidationError(
                "Solo se pueden modificar alquileres reservados."
            )

        if fin < inicio:
            raise serializers.ValidationError(
                "La fecha final no puede ser anterior a la fecha inicial."
            )

        if not self.instance and inicio < date.today():
            raise serializers.ValidationError(
                "La fecha inicial no puede estar en el pasado."
            )

        if vehiculo.estado == Vehiculo.Estado.MANTENIMIENTO:
            raise serializers.ValidationError(
                "El vehículo está en mantenimiento."
            )

        choque = (
            Alquiler.objects.filter(
                vehiculo=vehiculo,
                estado__in=ESTADOS_VIGENTES,
                fecha_inicio__lte=fin,
                fecha_fin__gte=inicio,
            )
            .exclude(
                pk=self.instance.pk if self.instance else None
            )
            .exists()
        )

        if choque:
            raise serializers.ValidationError(
                "El vehículo ya tiene un alquiler en esas fechas."
            )

        return attrs


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [RolePermission]

    roles_read = [ASESOR, JEFE_FLOTA, CLIENTE]
    roles_write = [JEFE_FLOTA]


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.select_related("categoria").all()
    serializer_class = VehiculoSerializer
    permission_classes = [RolePermission]

    roles_read = [ASESOR, JEFE_FLOTA, CLIENTE]
    roles_write = [JEFE_FLOTA]


class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.select_related("vehiculo").all()
    serializer_class = MantenimientoSerializer
    permission_classes = [RolePermission]

    roles_read = [ASESOR, JEFE_FLOTA]
    roles_write = [JEFE_FLOTA]
