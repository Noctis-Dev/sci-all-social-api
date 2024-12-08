# Sci-All Social API

Esta API permite gestionar publicaciones, comentarios y servicios relacionados para una red social científica. Desarrollada con Python, ofrece una arquitectura limpia y modular que facilita el mantenimiento y la expansión.

## Tecnologías
- **Python 3.x**
- **FastAPI** (para endpoints de API RESTful)
- **SQLAlchemy** (manejo de base de datos)
- **PostgreSQL** (base de datos por defecto)

## Requisitos previos
- **Python 3.10 o superior**. Puedes instalarlo desde [aquí](https://www.python.org/downloads/).
- **pip** para manejar dependencias. 

## Configuración inicial

### Clonar el repositorio
1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Noctis-Dev/sci-all-social-api.git
   cd sci-all-social-api
   ```

2. **Configura el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos en el archivo `.env`:**
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```env
   DATABASE_URL=postgresql://postgres:adminadmin@localhost:5432/sci_all_social
   ```

5. **Inicia la base de datos (opcional, usando Docker):**
   ```bash
   docker run --name sci_all_social_postgres -e POSTGRES_PASSWORD=adminadmin -p 5432:5432 -d postgres
   ```

6. **Ejecuta las migraciones:**
   ```bash
   python manage.py db upgrade
   ```

7. **Inicia el servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Accede a la API:**
   Abre [http://localhost:8000/docs](http://localhost:8000/docs) para ver la documentación interactiva generada por Swagger.

### Notas Finales
- Este proyecto utiliza PostgreSQL como base de datos por defecto. Si prefieres otra base de datos, asegúrate de modificar la configuración en el archivo `.env`.
- Si encuentras algún problema, por favor abre un _issue_ en el repositorio.

