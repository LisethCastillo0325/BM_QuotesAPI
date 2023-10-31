
# Comandos Docker Compose

### En el ambiente Local

Construir proyecto

    docker-compose build

Crear migraciones

    docker-compose run --rm django python manage.py makemigrations

    docker-compose run --rm django python manage.py migrate

Crear super usuario

    docker-compose run --rm django python manage.py createsuperuser


Ejecutar proyecto

    docker-compose up


Ejecutar pruebas unitarias

    docker compose run --rm django pytest


Acceder al Admin de Django

    http://localhost:8000/ms_quotes/app/admin/login/


Acceder a documentación con Swagger

    http://localhost:8000/swagger/
