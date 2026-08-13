#!/usr/bin/env bash
# Script que Render ejecuta al construir el backend de FitFlow.
# Si algún comando falla, el despliegue se detiene.
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Recolecta los estáticos del admin y de Jazzmin para que WhiteNoise los sirva.
python manage.py collectstatic --no-input

# Aplica las migraciones sobre la base de datos PostgreSQL de Render.
python manage.py migrate

# ---------------------------------------------------------------------------
# Creación del superusuario.
#
# El plan gratuito de Render no da acceso a una consola, así que el usuario
# administrador se crea aquí. Django lee las tres variables DJANGO_SUPERUSER_*
# que se configuran desde el panel de Render; nunca se escriben en el código.
#
# Si el usuario ya existe el comando falla, y el "|| echo" evita que eso
# tumbe todo el despliegue en los builds siguientes.
# ---------------------------------------------------------------------------
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --no-input || echo "El superusuario ya existía; se continúa."
else
  echo "Sin variables DJANGO_SUPERUSER_*: no se crea el administrador."
fi

# Carga datos de ejemplo sólo si SEED_DEMO está en True.
if [ "$SEED_DEMO" = "True" ]; then
  python manage.py seed_demo || echo "No se pudieron cargar los datos de ejemplo."
fi
