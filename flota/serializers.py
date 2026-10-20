from rest_framework import serializers
from .models import Categoria, Vehiculo, Mantenimiento


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"

    def validate_tarifa_diaria(self, value):
        if value <= 0:
            raise serializers.ValidationError("La tarifa diaria debe ser mayor a 0.")
        return value


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = "__all__"

    def validate_anio(self, value):
        if value < 1990 or value > 2030:
            raise serializers.ValidationError("El año debe estar entre 1990 y 2030.")
        return value


class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = "__all__"

    def validate_costo(self, value):
        if value < 0:
            raise serializers.ValidationError("El costo no puede ser negativo.")
        return value