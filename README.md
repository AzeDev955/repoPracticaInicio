# 🚀 Práctica de Docker, Pytest y Hooks de Git

Este proyecto es una aplicación web básica de Flask que sirve como demostración de un flujo de desarrollo moderno y contenerizado.

El objetivo es crear un entorno de desarrollo **idéntico**, **reproducible** y **automatizado** para todos los miembros del equipo. Esto se logra usando Docker para la contenerización, `pytest` para las pruebas y `black` para el formateo de código, todo reforzado automáticamente mediante un _hook_ de Git `pre-commit`.

---

## 📋 Características Principales

- **Entorno de Producción (Dockerfile)**: Una imagen optimizada (`python:3.11-slim`) lista para desplegar.
- **Entorno de Desarrollo (docker-compose.yml)**: Un servicio `dev` que monta el código fuente local e incluye herramientas de testing (`pytest`) y formateo (`black`).
- **Testing**: Suite de tests configurada en `tests/` y gestionada por `pytest.ini`.
- **Control de Calidad Automático**: Un _hook_ `pre-commit` que impide que se suba código mal formateado o que rompa los tests.

---

## 🏁 Cómo levantar la App (Modo Producción)

Estos comandos simulan cómo se ejecutaría la aplicación en un servidor o en producción.

1.  **Construir la imagen de Docker:**

    ```sh
    docker build -t mi-app:1.0 .
    ```

2.  **Ejecutar el contenedor:**
    ```sh
    docker run --rm -p 8000:8000 mi-app:1.0
    ```

Tras ejecutar el comando, la aplicación estará disponible en tu navegador en `http://localhost:8000`.

---

## 🛠️ Entorno de Desarrollo

Para desarrollar, no usamos el `Dockerfile` principal, sino el servicio `dev` definido en `docker-compose.yml`.

### 1. Construir la imagen de desarrollo

Este comando solo necesitas ejecutarlo una vez, o cada vez que modifiques `requirements.txt`:

```sh
docker compose build dev
```

### 2. Usar el entorno de desarrollo

Todos los comandos de desarrollo (como instalar paquetes, correr tests, etc.) deben ejecutarse dentro de este contenedor. La forma de hacerlo es prefijando tus comandos con docker compose run ....

Ejemplo: Abrir una shell interactiva

Si quieres "entrar" al contenedor para explorar o ejecutar múltiples comandos:

Bash

docker compose run --rm dev bash
Ejemplo: Comprobar la versión de Python

Para ejecutar un solo comando y salir:

Bash

docker compose run --rm -T dev python --version
Desglose del comando:

docker compose run: Ejecuta un contenedor para un servicio.

--rm: Elimina el contenedor automáticamente al terminar.

-T: (Opcional pero recomendado para scripts) Deshabilita la asignación de una TTY (terminal).

dev: El nombre del servicio a usar (definido en docker-compose.yml).

python --version: El comando a ejecutar dentro del contenedor.

✅ Tests y Formateo de Código
Gracias al entorno de desarrollo, no necesitas tener pytest o black instalados en tu máquina local.

Ejecutar Tests
Para ejecutar la suite completa de tests definida en pytest.ini:

Bash

docker compose run --rm -T dev pytest
Formatear el Código (Black)
Para comprobar si el código necesita formateo (no modifica archivos):

Bash

docker compose run --rm -T dev black --check .
Para formatear automáticamente todos los archivos .py:

Bash

docker compose run --rm -T dev black .
🛡️ Hook Pre-commit Automático
Este repositorio incluye un "guardián" automático para mantener la calidad del código.

¿Qué hace?
El script .git/hooks/pre-commit se ejecuta automáticamente cada vez que intentas hacer git commit.

Su trabajo es:

Formatear el código: Ejecuta black . dentro del contenedor. Si tu código estaba mal formateado, black lo arreglará por ti.

Ejecutar los tests: Ejecuta pytest dentro del contenedor.

Decidir:

Si los tests fallan o black encuentra un error de sintaxis, el commit se cancela.

Si todo está correcto, el commit se crea con éxito.

Importante: ¡Paso de configuración único!

Git no ejecuta hooks si no tienen permisos de ejecución. Después de clonar el repositorio, ejecuta este comando una sola vez para activar el hook:

Bash

chmod +x .git/hooks/pre-commit
