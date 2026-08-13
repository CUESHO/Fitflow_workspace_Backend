from django.db import models
from django.utils import timezone


class Miembro(models.Model):
    """Persona inscrita en el gimnasio."""

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estatura_cm = models.IntegerField(null=True, blank=True)
    notas_medicas = models.TextField(blank=True)
    estado_activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellidos", "nombre"]
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"


class TipoMembresia(models.Model):
    """Catálogo de planes: Mensual, Anual, Estudiante, etc."""

    nombre = models.CharField(max_length=100, unique=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    dias_duracion = models.IntegerField(default=30)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["costo"]
        verbose_name = "Tipo de membresía"
        verbose_name_plural = "Tipos de membresía"

    def __str__(self):
        return f"{self.nombre} - ${self.costo}"


class Area(models.Model):
    """Zonas del gimnasio: Pesas, Cardio, Spinning..."""

    nombre = models.CharField(max_length=100, unique=True)
    capacidad_maxima = models.IntegerField()
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

    def __str__(self):
        return self.nombre


class Suscripcion(models.Model):
    """Relaciona un miembro con el plan que pagó y su vigencia."""

    miembro = models.ForeignKey(
        Miembro, on_delete=models.CASCADE, related_name="suscripciones"
    )
    tipo = models.ForeignKey(
        TipoMembresia,
        on_delete=models.RESTRICT,
        related_name="suscripciones",
        verbose_name="Tipo de membresía",
    )
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"

    def __str__(self):
        return f"{self.miembro} - Vence: {self.fecha_fin}"

    @property
    def vigente(self):
        """True si la suscripción está activa y aún no vence."""
        return self.activa and self.fecha_fin >= timezone.localdate()


class RegistroAcceso(models.Model):
    """Entrada y salida de un miembro a un área del gimnasio."""

    miembro = models.ForeignKey(
        Miembro, on_delete=models.CASCADE, related_name="accesos"
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accesos",
    )
    fecha_hora_entrada = models.DateTimeField(default=timezone.now)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_hora_entrada"]
        verbose_name = "Registro de acceso"
        verbose_name_plural = "Registros de acceso"

    def __str__(self):
        return f"{self.miembro} - {self.fecha_hora_entrada:%d/%m/%Y %H:%M}"

    @property
    def sigue_dentro(self):
        """True mientras no se registre la salida."""
        return self.fecha_hora_salida is None
