
from rest_framework import serializers
from .models import Alquiler, AlquilerAccesorio


class AlquilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alquiler
        fields = "__all__"

    def validate(self, attrs):
        fecha_inicio = attrs.get(
            "fecha_inicio",
            getattr(self.instance, "fecha_inicio", None)
        )
        fecha_fin = attrs.get(
            "fecha_fin",
            getattr(self.instance, "fecha_fin", None)
        )

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError(
                "La fecha final no puede ser anterior a la fecha inicial."
            )

        return attrs


class AlquilerAccesorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlquilerAccesorio
        fields = "__all__"

    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "La cantidad debe ser al menos 1."
            )
        return value


