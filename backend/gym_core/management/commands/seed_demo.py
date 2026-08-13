"""Carga datos de ejemplo en FitFlow.

Uso:
    python manage.py seed_demo
    python manage.py seed_demo --limpiar   (borra los datos previos)
"""

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from gym_core.models import Area, Miembro, RegistroAcceso, Suscripcion, TipoMembresia

MIEMBROS = [
    ("Aarón", "Castañeda", "aaron.castaneda@fitflow.mx", "8110000001"),
    ("Lucía", "Ramírez", "lucia.ramirez@fitflow.mx", "8110000002"),
    ("Diego", "Hernández", "diego.hernandez@fitflow.mx", "8110000003"),
    ("Mariana", "Ortiz", "mariana.ortiz@fitflow.mx", "8110000004"),
    ("Sofía", "Delgado", "sofia.delgado@fitflow.mx", "8110000005"),
    ("Bruno", "Salazar", "bruno.salazar@fitflow.mx", "8110000006"),
]

TIPOS = [
    ("Mensual", 450.00, 30, "Acceso ilimitado durante un mes."),
    ("Trimestral", 1200.00, 90, "Tres meses con 10% de descuento."),
    ("Anual", 4200.00, 365, "Plan anual con acceso a todas las áreas."),
    ("Estudiante", 300.00, 30, "Tarifa especial presentando credencial vigente."),
]

AREAS = [
    ("Pesas", 40, "Zona de peso libre y máquinas de fuerza."),
    ("Cardio", 30, "Caminadoras, elípticas y bicicletas fijas."),
    ("Spinning", 20, "Salón de ciclismo indoor."),
    ("Funcional", 25, "Entrenamiento funcional y cross training."),
]


class Command(BaseCommand):
    help = "Carga datos de ejemplo para demostrar el CRUD de FitFlow."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Elimina los registros existentes antes de cargar los nuevos.",
        )

    def handle(self, *args, **opciones):
        if opciones["limpiar"]:
            RegistroAcceso.objects.all().delete()
            Suscripcion.objects.all().delete()
            Miembro.objects.all().delete()
            Area.objects.all().delete()
            TipoMembresia.objects.all().delete()
            self.stdout.write(self.style.WARNING("Datos anteriores eliminados."))

        tipos = [
            TipoMembresia.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "costo": costo,
                    "dias_duracion": dias,
                    "descripcion": descripcion,
                },
            )[0]
            for nombre, costo, dias, descripcion in TIPOS
        ]

        areas = [
            Area.objects.get_or_create(
                nombre=nombre,
                defaults={"capacidad_maxima": capacidad, "descripcion": descripcion},
            )[0]
            for nombre, capacidad, descripcion in AREAS
        ]

        miembros = []
        for nombre, apellidos, email, telefono in MIEMBROS:
            miembro, _ = Miembro.objects.get_or_create(
                email=email,
                defaults={
                    "nombre": nombre,
                    "apellidos": apellidos,
                    "telefono": telefono,
                    "fecha_nacimiento": timezone.localdate()
                    - timedelta(days=random.randint(6600, 14000)),
                    "peso_kg": round(random.uniform(55, 95), 2),
                    "estatura_cm": random.randint(155, 190),
                    "estado_activo": True,
                },
            )
            miembros.append(miembro)

        hoy = timezone.localdate()
        for miembro in miembros:
            tipo = random.choice(tipos)
            Suscripcion.objects.get_or_create(
                miembro=miembro,
                tipo=tipo,
                defaults={
                    "fecha_inicio": hoy - timedelta(days=random.randint(1, 20)),
                    "fecha_fin": hoy + timedelta(days=tipo.dias_duracion),
                    "activa": True,
                },
            )

        # Algunos accesos ya cerrados y otros con el miembro todavía dentro.
        if not RegistroAcceso.objects.exists():
            ahora = timezone.now()
            for indice, miembro in enumerate(miembros):
                entrada = ahora - timedelta(hours=random.randint(1, 48))
                sigue_dentro = indice % 3 == 0
                RegistroAcceso.objects.create(
                    miembro=miembro,
                    area=random.choice(areas),
                    fecha_hora_entrada=entrada,
                    fecha_hora_salida=None
                    if sigue_dentro
                    else entrada + timedelta(minutes=random.randint(40, 120)),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo: {Miembro.objects.count()} miembros, "
                f"{TipoMembresia.objects.count()} tipos de membresía, "
                f"{Area.objects.count()} áreas, "
                f"{Suscripcion.objects.count()} suscripciones, "
                f"{RegistroAcceso.objects.count()} accesos."
            )
        )
