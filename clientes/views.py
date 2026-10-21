from rest_framework import viewsets
from config.permissions import ASESOR, CLIENTE, grupos
from .models import Cliente
from .serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    roles_read = [ASESOR, CLIENTE]
    roles_write = [ASESOR]
    search_fields = ["nombres", "apellidos", "numero_documento", "correo"]
    ordering_fields = ["apellidos", "nombres"]

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        if not u.is_superuser and grupos(u) == {CLIENTE}:   # el cliente solo ve el suyo
            return qs.filter(usuario=u)
        return qs