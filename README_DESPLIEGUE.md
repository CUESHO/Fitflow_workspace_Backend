# Despliegue de FitFlow en Render

El proyecto son **dos repositorios separados**, así que en Render se crean
**dos servicios**: el backend de Django y el sitio estático de Angular.

---

## 1. Backend (Django REST Framework + PostgreSQL)

### Opción A — Con el archivo `render.yaml` (recomendada)

1. Sube el repositorio del backend a GitHub.
2. En Render entra a **New → Blueprint** y selecciona el repositorio.
3. Render lee `render.yaml` y crea solos la base de datos y el servicio web.
4. Espera a que termine el despliegue.

### Opción B — Manual desde el panel

1. **New → PostgreSQL**, plan *Free*, nombre `fitflow-db`.
2. **New → Web Service**, selecciona el repositorio del backend y configura:

   | Campo | Valor |
   |---|---|
   | Root Directory | `backend` |
   | Runtime | Python 3 |
   | Build Command | `chmod +x build.sh && ./build.sh` |
   | Start Command | `gunicorn fitflow_api.wsgi:application` |

3. En **Environment** agrega estas variables:

   | Variable | Valor |
   |---|---|
   | `DATABASE_URL` | La *Internal Database URL* de `fitflow-db` |
   | `SECRET_KEY` | Una cadena larga y aleatoria |
   | `ENV` | `prod` |
   | `DEBUG` | `False` |
   | `PYTHON_VERSION` | `3.12.7` |
   | `ALLOWED_ORIGINS` | La URL del frontend, ej. `https://fitflow-frontend.onrender.com` |

### Crear el usuario administrador

El superusuario que creaste en tu computadora **no existe en Render**: allá la base
de datos es nueva y está vacía. Y como el plan gratuito de Render no incluye
consola (Shell), no se puede ejecutar `createsuperuser` a mano.

Por eso `build.sh` lo crea automáticamente a partir de tres variables de entorno
que tú defines en el panel de Render. Nunca se escriben en el repositorio:

| Variable | Ejemplo |
|---|---|
| `DJANGO_SUPERUSER_USERNAME` | `aaron` |
| `DJANGO_SUPERUSER_EMAIL` | `tucorreo@ejemplo.com` |
| `DJANGO_SUPERUSER_PASSWORD` | *(una contraseña que sólo tú elijas)* |

Con esas variables definidas, el primer despliegue deja la cuenta lista para
entrar en `https://TU-BACKEND.onrender.com/admin/`.

Si en algún momento quieres cambiar la contraseña, actualiza la variable, borra
el usuario desde el panel de administración y vuelve a lanzar el despliegue.

### Datos de ejemplo

Si quieres que la base arranque con miembros, áreas y accesos de ejemplo para la
presentación, pon la variable `SEED_DEMO` en `True` y vuelve a desplegar.
Déjala en `False` cuando ya no la necesites.

---

## 2. Frontend (Angular)

1. Antes de subir, edita `src/environments/environment.prod.ts` y pon la URL
   real de tu backend:

   ```ts
   export const environment = {
     produccion: true,
     apiUrl: 'https://TU-BACKEND.onrender.com/api',
   };
   ```

2. Sube el repositorio del frontend a GitHub.
3. En Render: **New → Static Site**, selecciona el repositorio y configura:

   | Campo | Valor |
   |---|---|
   | Build Command | `npm ci && npm run build` |
   | Publish Directory | `dist/fitflow-frontend/browser` |

4. En **Redirects/Rewrites** agrega una regla para que funcionen las rutas
   de Angular al recargar la página:

   | Source | Destination | Action |
   |---|---|---|
   | `/*` | `/index.html` | Rewrite |

---

## 3. Paso final importante

Cuando Render te dé la URL del frontend, regresa al **backend** y actualiza la
variable de entorno `ALLOWED_ORIGINS` con esa URL exacta. Sin este paso el
navegador bloqueará las peticiones por CORS y las tablas se verán vacías.

---

## Notas

- La base de datos PostgreSQL gratuita de Render **expira a los 30 días**.
  Conviene desplegar cerca de la fecha de entrega.
- El plan gratuito duerme el servicio tras un rato sin uso: la primera carga
  puede tardar ~50 segundos. Vale la pena abrir la página unos minutos antes
  de presentar.
