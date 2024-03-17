FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /hotel-service

COPY ./hotel-catalog-service/requirements.txt /hotel-service/
RUN pip install --no-cache-dir -r /hotel-service/requirements.txt

COPY ./hotel-catalog-service/app /hotel-service/app
COPY ./hotel-catalog-service/alembic /hotel-service/alembic
COPY ./hotel-catalog-service/alembic.ini /hotel-service/alembic.ini

EXPOSE 82

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
