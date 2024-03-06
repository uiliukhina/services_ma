FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /booking-service

COPY ./booking-service/requirements.txt /booking-service/
RUN pip install --no-cache-dir -r /booking-service/requirements.txt

COPY ./booking-service/app /booking-service/app

EXPOSE 81

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 81"]
