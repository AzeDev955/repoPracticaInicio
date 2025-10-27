# Ejercicio Docker + precommits + flask

# Práctica: Contenerización, linting y tests con Docker + hooks de Git

Para realizar esta práctica hay que seguir las convenciones de ramas y commits previamente establecidas.

## Código inicial del repo

- `app.py`
- `requirements.txt`
- `Dockerfile`

---

## Pasos

### 1) Revisar el Dockerfile de ejecución (producción simple)

1. Abre `Dockerfile` y confirma que:

   ```docker
   FROM python:3.11-slim

   WORKDIR /app

   COPY . .

   RUN pip install --no-cache-dir -r requirements.txt

   EXPOSE 8000

   CMD ["python", "app.py"]

   ```

2. Construye y prueba:

   ```bash
   docker build -t mi-app:1.0 .
   docker run --rm -p 8000:8000 mi-app:1.0

   ```

3. Verifica en el navegador `http://localhost:8000`.
4. Haz una captura a lo que salga en la consola. Explica que hacen exactamente los dos comandos de docker que has utilizado. Si no entiendes las opciones busca información sobre ellas.

---

### 2) Crear `.dockerignore`

1. Crea `.dockerignore` en la raíz con:

   ```
   __pycache__/
   *.pyc
   *.pyo
   *.log
   .env
   .git
   .gitignore
   venv/
   node_modules/
   Dockerfile.dev
   docker-compose.yml
   Dockerfile
   ```

2. ¿Para que sirve este archivo?

---

### 3) Crear Dockerfile de desarrollo

1. Crea `Dockerfile.dev`:

   ```docker
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt
   RUN pip install --no-cache-dir black pytest
   CMD ["bash"]
   ```

2. ¿Para qué es útil un Dockerfile de desarrollo?

---

### 4) Crear docker-compose para el servicio de desarrollo

1. Crea `docker-compose.yml`:

   ```yaml
   services:
     dev:
       build:
         context: .
         dockerfile: Dockerfile.dev
       volumes:
         - .:/app
       working_dir: /app
       environment:
         - PYTHONPATH=/app
   ```

2. Construye la imagen de dev:

   ```bash
   docker compose build dev
   ```

3. Prueba una shell dentro:

   ```bash
   docker compose run --rm -T dev python --version
   ```

4. Haz captura a la salida del último comando y explica para que sirven los 2 comandos de docker utililzados. ¿Debería salir una versión diferente en función del ordenador en el que lo uses?

---

### 5) Añadir pytest.ini y primer test

1. Crea `pytest.ini`:

   ```
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_functions = test_*
   addopts = -q

   ```

2. Crea carpeta `tests/` y archivo `tests/test_app.py`:

   ```python
   from app import app as flask_app

   def test_home_ok():
       flask_app.testing = True
       client = flask_app.test_client()
       resp = client.get("/")
       assert resp.status_code == 200

   ```

3. Ejecuta los tests dentro del contenedor:

   ```bash
   docker compose run --rm -T dev pytest
   ```

4. Haz captura del resultado

---

### 6) Añadir Black y comprobar formato

1. Verifica Black:

   ```bash
   docker compose run --rm -T dev black --check .
   ```

2. Si falla, autoformatea:

   ```bash
   docker compose run --rm -T dev black .
   ```

---

### 7) Preparar hook pre-commit (shell)

1. Crea el hook `.git/hooks/pre-commit`

```bash
#!/bin/sh
echo "Ejecutando pre-commit con Docker..."

# Formato
docker compose run --rm -T dev black .
if [ $? -ne 0 ]; then
  echo "Código mal formateado"
  exit 1
fi

# Tests
echo "Ejecutando tests..."
TEST_OUTPUT=$(docker compose run --rm -T dev sh -lc 'pytest -q --disable-warnings --color=no')
TEST_EXIT=$?
echo "$TEST_OUTPUT"
if [ $TEST_EXIT -ne 0 ]; then
  echo "Algunos tests fallaron."
  exit 1
fi

exit 0

```

2. ¿Cuándo se ejecutará esto?

---

### 8) Probar el hook

1. Prueba sin cambios con un commit vacío:

   ```bash
   git commit --allow-empty -m "test: prueba pre-commit"

   ```

2. Introduce un error de formato en un `.py` y vuelve a intentar comitear para comprobar que bloquea el commit.
3. Vuelve a hacer el commit
4. ¿Cuál ha sido el resultado?¿Qué ha pasado con el archivo .py?

---

### 9) Documentar en README.md

Crea `README.md` con:

- Información sobre el proyecto
- Cómo levantar la app.
- Cómo usar el entorno de desarrollo (`docker compose run ...`).
- Cómo ejecutar tests y formateo.
- Cómo actúa el pre-commit.
