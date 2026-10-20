from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, VehiculoViewSet, MantenimientoViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("vehiculos", VehiculoViewSet, basename="vehiculo")
router.register("mantenimientos", MantenimientoViewSet, basename="mantenimiento")

urlpatterns = router.urls