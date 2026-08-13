"""
Rutas del proyecto FitFlow.

El DefaultRouter de DRF genera automáticamente las rutas CRUD de cada modelo:
    GET    /api/miembros/       -> listar
    POST   /api/miembros/       -> crear
    GET    /api/miembros/{id}/  -> recuperar
    PUT    /api/miembros/{id}/  -> actualizar
    DELETE /api/miembros/{id}/  -> eliminar
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from gym_core.views import (
    AreaViewSet,
    MiembroViewSet,
    RegistroAccesoViewSet,
    SuscripcionViewSet,
    TipoMembresiaViewSet,
)

router = DefaultRouter()
router.register(r"miembros", MiembroViewSet)
router.register(r"tipos-membresia", TipoMembresiaViewSet)
router.register(r"areas", AreaViewSet)
router.register(r"suscripciones", SuscripcionViewSet)
router.register(r"accesos", RegistroAccesoViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # La raíz del sitio lleva al panel de administración.
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
