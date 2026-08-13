from rest_framework import viewsets
from .models import Miembro, TipoMembresia, Suscripcion, Area, RegistroAcceso
from .serializers import (MiembroSerializer, TipoMembresiaSerializer, 
                          SuscripcionSerializer, AreaSerializer, RegistroAccesoSerializer)

class MiembroViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer

class TipoMembresiaViewSet(viewsets.ModelViewSet):
    queryset = TipoMembresia.objects.all()
    serializer_class = TipoMembresiaSerializer

class SuscripcionViewSet(viewsets.ModelViewSet):
    queryset = Suscripcion.objects.all()
    serializer_class = SuscripcionSerializer

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class RegistroAccesoViewSet(viewsets.ModelViewSet):
    queryset = RegistroAcceso.objects.all()
    serializer_class = RegistroAccesoSerializer