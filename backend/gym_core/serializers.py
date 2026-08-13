from rest_framework import serializers

from .models import Area, Miembro, RegistroAcceso, Suscripcion, TipoMembresia


class MiembroSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model = Miembro
        fields = "__all__"


class TipoMembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMembresia
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class SuscripcionSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para que Angular muestre nombres y no sólo IDs.
    miembro_nombre = serializers.CharField(
        source="miembro.nombre_completo", read_only=True
    )
    tipo_nombre = serializers.CharField(source="tipo.nombre", read_only=True)
    vigente = serializers.BooleanField(read_only=True)

    class Meta:
        model = Suscripcion
        fields = "__all__"

    def validate(self, data):
        """La fecha de fin nunca puede ser anterior a la de inicio."""
        inicio = data.get("fecha_inicio", getattr(self.instance, "fecha_inicio", None))
        fin = data.get("fecha_fin", getattr(self.instance, "fecha_fin", None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError(
                {"fecha_fin": "La fecha de fin debe ser posterior a la de inicio."}
            )
        return data


class RegistroAccesoSerializer(serializers.ModelSerializer):
    miembro_nombre = serializers.CharField(
        source="miembro.nombre_completo", read_only=True
    )
    area_nombre = serializers.CharField(source="area.nombre", read_only=True)
    sigue_dentro = serializers.BooleanField(read_only=True)

    class Meta:
        model = RegistroAcceso
        fields = "__all__"

    def validate(self, data):
        """No se puede registrar una salida anterior a la entrada."""
        entrada = data.get(
            "fecha_hora_entrada", getattr(self.instance, "fecha_hora_entrada", None)
        )
        salida = data.get(
            "fecha_hora_salida", getattr(self.instance, "fecha_hora_salida", None)
        )
        if entrada and salida and salida < entrada:
            raise serializers.ValidationError(
                {"fecha_hora_salida": "La salida debe ser posterior a la entrada."}
            )
        return data
