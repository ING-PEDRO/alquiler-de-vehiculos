from django.shortcuts import render
from rest_framework import viewsets
from .models import Categoria, Vehiculo, Mantenimiento
from .serializers import (
    CategoriaSerializer,
    VehiculoSerializer,
    MantenimientoSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.select_related("categoria").all()
    serializer_class = VehiculoSerializer


class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.select_related("vehiculo").all()
    serializer_class = MantenimientoSerializer
# Create your views here.
