from rest_framework import viewsets
from .models import Accesorio
from .serializers import AccesorioSerializer


class AccesorioViewSet(viewsets.ModelViewSet):
    queryset = Accesorio.objects.all()
    serializer_class = AccesorioSerializer