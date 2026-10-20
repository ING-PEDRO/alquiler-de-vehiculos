
from rest_framework.routers import DefaultRouter
from .views import AlquilerViewSet, AlquilerAccesorioViewSet

router = DefaultRouter()
router.register(
    "alquileres",
    AlquilerViewSet,
    basename="alquiler"
)
router.register(
    "alquiler-accesorios",
    AlquilerAccesorioViewSet,
    basename="alquiler-accesorio"
)

urlpatterns = router.urls
