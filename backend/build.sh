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
