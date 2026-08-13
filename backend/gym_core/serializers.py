from rest_framework import serializers
from .models import Miembro, TipoMembresia, Suscripcion, Area, RegistroAcceso

class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = '__all__'

class TipoMembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMembresia
        fields = '__all__'

class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class RegistroAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAcceso
        fields = '__all__'