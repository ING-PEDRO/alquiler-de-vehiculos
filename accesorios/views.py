from rest_framework import viewsets
from config.permissions import ASESOR, CLIENTE, JEFE_FLOTA
from .models import Accesorio
from .serializers import AccesorioSerializer


class AccesorioViewSet(viewsets.ModelViewSet):
    queryset = Accesorio.objects.all()
    serializer_class = AccesorioSerializer
    roles_read = [ASESOR, JEFE_FLOTA, CLIENTE]
    roles_write = [JEFE_FLOTA]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre", "precio_dia", "stock"]