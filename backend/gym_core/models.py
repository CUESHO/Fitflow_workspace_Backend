from django.db import models

class Miembro(models.Model):
    # Campos básicos (Strings)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    
    # Variedad de tipos de datos (Fechas, Booleanos, Decimales)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estatura_cm = models.IntegerField(null=True, blank=True)
    
    # Control de acceso y biometría (Booleanos y Strings)
    huella_biometrica_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    estado_activo = models.BooleanField(default=True)
    
    # Textos largos para edge cases
    notas_medicas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} - {self.email}"
# Create your models here.
