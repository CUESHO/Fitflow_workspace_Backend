from django.db import models
from django.utils import timezone

# 1. TU MODELO EXISTENTE (Déjalo como lo tienes, aquí solo lo pongo de referencia)
class Miembro(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    estado_activo = models.BooleanField(default=True)
    # ... los demás campos que ya tenías

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# 2. CATÁLOGO DE MEMBRESÍAS
class TipoMembresia(models.Model):
    nombre = models.CharField(max_length=100) # Ej. Mensual, Anual, Estudiante
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    dias_duracion = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.nombre} - ${self.costo}"

# 3. SUSCRIPCIONES (Para saber si pagaron)
class Suscripcion(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='suscripciones')
    tipo = models.ForeignKey(TipoMembresia, on_delete=models.RESTRICT)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.miembro.nombre} - Vence: {self.fecha_fin}"

# 4. ÁREAS DEL GIMNASIO (Vital para la telemetría y predicción)
class Area(models.Model):
    nombre = models.CharField(max_length=100) # Ej. Pesas, Cardio, Spinning
    capacidad_maxima = models.IntegerField()
    
    def __str__(self):
        return self.nombre

# 5. EL MOTOR DE ACCESOS (Ahora sabe a qué área entraron)
class RegistroAcceso(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='accesos')
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_hora_entrada = models.DateTimeField(default=timezone.now)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.miembro.nombre} - Entrada: {self.fecha_hora_entrada.strftime('%Y-%m-%d %H:%M')}"