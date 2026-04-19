from rest_framework.routers import DefaultRouter
from .views import MedicoViewSet, EspecialidadeViewSet

router = DefaultRouter()
router.register('medicos', MedicoViewSet)
router.register('especialidades', EspecialidadeViewSet)

urlpatterns = router.urls