from django.contrib import admin

from .models import Area, Miembro, RegistroAcceso, Suscripcion, TipoMembresia


@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellidos", "email", "telefono", "estado_activo")
    list_display_links = ("id", "nombre")
    search_fields = ("nombre", "apellidos", "email", "telefono")
    list_filter = ("estado_activo", "fecha_registro")
    ordering = ("apellidos", "nombre")
    list_per_page = 25


@admin.register(TipoMembresia)
class TipoMembresiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "costo", "dias_duracion")
    list_display_links = ("id", "nombre")
    search_fields = ("nombre", "descripcion")
    list_filter = ("dias_duracion",)
    ordering = ("costo",)
    list_per_page = 25


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "capacidad_maxima")
    list_display_links = ("id", "nombre")
    search_fields = ("nombre", "descripcion")
    list_filter = ("capacidad_maxima",)
    ordering = ("nombre",)
    list_per_page = 25


@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ("id", "miembro", "tipo", "fecha_inicio", "fecha_fin", "activa")
    list_display_links = ("id", "miembro")
    search_fields = ("miembro__nombre", "miembro__apellidos", "tipo__nombre")
    list_filter = ("activa", "tipo", "fecha_inicio")
    ordering = ("-fecha_inicio",)
    autocomplete_fields = ("miembro", "tipo")
    list_per_page = 25


@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ("id", "miembro", "area", "fecha_hora_entrada", "fecha_hora_salida")
    list_display_links = ("id", "miembro")
    search_fields = ("miembro__nombre", "miembro__apellidos", "area__nombre")
    list_filter = ("area", "fecha_hora_entrada")
    ordering = ("-fecha_hora_entrada",)
    autocomplete_fields = ("miembro", "area")
    date_hierarchy = "fecha_hora_entrada"
    list_per_page = 25
