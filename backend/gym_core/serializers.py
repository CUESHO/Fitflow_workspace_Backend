from rest_framework import serializers
from .models import Miembro

class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = '__all__' # Queremos que Angular reciba todos los datos (biometría, fechas, etc)