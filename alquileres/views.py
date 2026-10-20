
from rest_framework import viewsets
from .models import Alquiler, AlquilerAccesorio
from .serializers import (
    AlquilerSerializer,
    AlquilerAccesorioSerializer,
)


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.select_related(
        "cliente", "vehiculo"
    ).all()
    serializer_class = AlquilerSerializer


class AlquilerAccesorioViewSet(viewsets.ModelViewSet):
    queryset = AlquilerAccesorio.objects.select_related(
        "alquiler", "accesorio"
    ).all()
    serializer_class = AlquilerAccesorioSerializer
