from rest_framework import serializers
from .models import Accesorio


class AccesorioSerializer(serializers.ModelSerializer):


    def validate_precio_dia(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio por dia debe ser mayor a 0.")
        return value
    class Meta:
        model = Accesorio
        fields = '__all__'