FROM python:3.9-buster

ENV PYTHONUNBUFFERED 1

ENV XDG_RUNTIME_DIR=/tmp

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

# Instalar librerias wkhtmltopdf
RUN apt-get update
RUN apt-get -f -y install wkhtmltopdf
RUN apt-get -y install zlib1g fontconfig libxrender1 libfreetype6 libxext6 libx11-6

WORKDIR /app

# Copiar el código fuente de la aplicación
COPY . .

ENTRYPOINT ["/entrypoint"]
