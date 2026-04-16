from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, AgendaViewSet, AgendamentoViewSet

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('agendas', AgendaViewSet)
router.register('agendamentos', AgendamentoViewSet)

urlpatterns = router.urls