from rest_framework import viewsets
from .models import Miembro
from .serializers import MiembroSerializer

class MiembroViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer