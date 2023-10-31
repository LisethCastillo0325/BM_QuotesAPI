FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

# Instalar librerias wkhtmltopdf
RUN apt-get update
RUN apt-get -f -y install wkhtmltopdf
RUN apt-get -y install zlib1g fontconfig libxrender1 libfreetype6 libxext6 libx11-6

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
