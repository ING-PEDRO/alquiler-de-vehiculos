from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from config.permissions import ASESOR, CLIENTE, JEFE_FLOTA, grupos
from flota.models import Vehiculo
from .models import Alquiler, AlquilerAccesorio
from .serializers import AlquilerAccesorioSerializer, AlquilerSerializer


def _solo_cliente(user):
    return not user.is_superuser and grupos(user) == {CLIENTE}


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = (Alquiler.objects.select_related("cliente", "vehiculo__categoria")
                .prefetch_related("accesorios_alquilados__accesorio").all())
    serializer_class = AlquilerSerializer
    roles_read = [ASESOR, JEFE_FLOTA, CLIENTE]
    roles_write = [ASESOR]
    roles_by_action = {
        "activar": [ASESOR, JEFE_FLOTA],
        "finalizar": [ASESOR, JEFE_FLOTA],
        "cancelar": [ASESOR],
    }
    search_fields = ["cliente__nombres", "cliente__apellidos", "vehiculo__placa"]
    ordering_fields = ["fecha_inicio", "fecha_fin", "id"]

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        if _solo_cliente(u):
            return qs.filter(cliente__usuario=u)
        p = self.request.query_params
        for campo, filtro in (("cliente", "cliente_id"), ("vehiculo", "vehiculo_id"), ("estado", "estado")):
            if p.get(campo):
                qs = qs.filter(**{filtro: p[campo]})
        return qs

    def destroy(self, request, *args, **kwargs):
        if self.get_object().estado != Alquiler.Estado.RESERVADO:
            raise ValidationError("Solo se pueden eliminar alquileres reservados; cancele los demas.")
        return super().destroy(request, *args, **kwargs)

    def _cambiar(self, alquiler, desde, hacia, estado_vehiculo=None):
        if alquiler.estado not in desde:
            raise ValidationError(
                f"No se puede pasar de '{alquiler.get_estado_display()}' a '{Alquiler.Estado(hacia).label}'.")
        with transaction.atomic():
            alquiler.estado = hacia
            alquiler.save(update_fields=["estado"])
            if estado_vehiculo:
                Vehiculo.objects.filter(pk=alquiler.vehiculo_id).update(estado=estado_vehiculo)
        return Response(self.get_serializer(alquiler).data)

    @action(detail=True, methods=["post"])
    def activar(self, request, pk=None):
        a = self.get_object()
        if a.vehiculo.estado != Vehiculo.Estado.DISPONIBLE:
            raise ValidationError("El vehiculo no esta disponible para entrega.")
        return self._cambiar(a, [Alquiler.Estado.RESERVADO], Alquiler.Estado.ACTIVO, Vehiculo.Estado.ALQUILADO)

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        return self._cambiar(self.get_object(), [Alquiler.Estado.ACTIVO],
                             Alquiler.Estado.FINALIZADO, Vehiculo.Estado.DISPONIBLE)

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        a = self.get_object()
        libera = Vehiculo.Estado.DISPONIBLE if a.estado == Alquiler.Estado.ACTIVO else None
        return self._cambiar(a, [Alquiler.Estado.RESERVADO, Alquiler.Estado.ACTIVO],
                             Alquiler.Estado.CANCELADO, libera)


class AlquilerAccesorioViewSet(viewsets.ModelViewSet):
    queryset = AlquilerAccesorio.objects.select_related("alquiler", "accesorio").all()
    serializer_class = AlquilerAccesorioSerializer
    roles_read = [ASESOR, JEFE_FLOTA, CLIENTE]
    roles_write = [ASESOR]

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        if _solo_cliente(u):
            return qs.filter(alquiler__cliente__usuario=u)
        if self.request.query_params.get("alquiler"):
            qs = qs.filter(alquiler_id=self.request.query_params["alquiler"])
        return qs