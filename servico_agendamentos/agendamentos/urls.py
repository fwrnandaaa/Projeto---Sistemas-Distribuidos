from rest_framework.routers import DefaultRouter
from .views import AgendaViewSet, AgendamentoViewSet

router = DefaultRouter()
router.register('agendas', AgendaViewSet)
router.register('agendamentos', AgendamentoViewSet)

urlpatterns = router.urls