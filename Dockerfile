FROM python:3.12
LABEL authors="sinortax"

WORKDIR /app

COPY ./tracker .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "-c", "python manage.py runserver"]
