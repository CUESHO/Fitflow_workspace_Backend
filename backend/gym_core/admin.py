from django.contrib import admin
from .models import Area, Miembro, RegistroAcceso, Suscripcion, TipoMembresia

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'capacidad_maxima')
    search_fields = ('nombre',)
    list_filter = ('capacidad_maxima',)
    ordering = ('nombre',)

@admin.register(TipoMembresia)
class TipoMembresiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'costo')
    search_fields = ('nombre',)
    list_filter = ('costo',)
    ordering = ('costo',)

@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellidos', 'email', 'estado')
    search_fields = ('nombre', 'apellidos', 'email', 'rfc') 
    list_filter = ('estado',)
    ordering = ('apellidos', 'nombre')

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'miembro', 'tipo_membresia', 'fecha_inicio', 'fecha_fin', 'estado')
    search_fields = ('miembro__nombre', 'miembro__apellidos')
    list_filter = ('estado', 'tipo_membresia')
    ordering = ('-fecha_inicio',)

@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ('id', 'miembro', 'area', 'fecha_hora') 
    search_fields = ('miembro__nombre', 'miembro__apellidos', 'area__nombre')
    list_filter = ('area', 'fecha_hora')
    ordering = ('-fecha_hora',)