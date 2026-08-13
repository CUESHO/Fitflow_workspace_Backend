from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Area, Miembro, RegistroAcceso, Suscripcion, TipoMembresia
from .serializers import (
    AreaSerializer,
    MiembroSerializer,
    RegistroAccesoSerializer,
    SuscripcionSerializer,
    TipoMembresiaSerializer,
)

# Los tres backends de filtrado que usa cada ViewSet:
#   DjangoFilterBackend -> ?estado_activo=true   (filtro exacto por campo)
#   SearchFilter        -> ?search=aaron         (búsqueda de texto)
#   OrderingFilter      -> ?ordering=-fecha      (ordenamiento)
FILTER_BACKENDS = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class MiembroViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    filter_backends = FILTER_BACKENDS
    filterset_fields = ["estado_activo"]
    search_fields = ["nombre", "apellidos", "email", "telefono"]
    ordering_fields = ["nombre", "apellidos", "fecha_registro"]
    ordering = ["apellidos", "nombre"]


class TipoMembresiaViewSet(viewsets.ModelViewSet):
    queryset = TipoMembresia.objects.all()
    serializer_class = TipoMembresiaSerializer
    filter_backends = FILTER_BACKENDS
    filterset_fields = ["dias_duracion"]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre", "costo", "dias_duracion"]
    ordering = ["costo"]


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filter_backends = FILTER_BACKENDS
    filterset_fields = ["capacidad_maxima"]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre", "capacidad_maxima"]
    ordering = ["nombre"]


class SuscripcionViewSet(viewsets.ModelViewSet):
    # select_related evita una consulta extra por fila al mostrar los nombres.
    queryset = Suscripcion.objects.select_related("miembro", "tipo").all()
    serializer_class = SuscripcionSerializer
    filter_backends = FILTER_BACKENDS
    filterset_fields = ["activa", "tipo", "miembro"]
    search_fields = ["miembro__nombre", "miembro__apellidos", "tipo__nombre"]
    ordering_fields = ["fecha_inicio", "fecha_fin"]
    ordering = ["-fecha_inicio"]


class RegistroAccesoViewSet(viewsets.ModelViewSet):
    queryset = RegistroAcceso.objects.select_related("miembro", "area").all()
    serializer_class = RegistroAccesoSerializer
    filter_backends = FILTER_BACKENDS
    filterset_fields = ["area", "miembro"]
    search_fields = ["miembro__nombre", "miembro__apellidos", "area__nombre"]
    ordering_fields = ["fecha_hora_entrada", "fecha_hora_salida"]
    ordering = ["-fecha_hora_entrada"]
