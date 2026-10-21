from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):


    def validate_numero_documento(self, value):
        value = value.strip()
        if not value.isalnum():
            raise serializers.ValidationError("El documento solo admite letras y numeros.")
        return value

    def validate_telefono(self, value):
        digitos = value.replace("+", "").replace(" ", "").replace("-", "")
        if not digitos.isdigit() or len(digitos) < 7:
            raise serializers.ValidationError("Telefono invalido.")
        return value
    class Meta:
        model = Cliente
        fields = "__all__"