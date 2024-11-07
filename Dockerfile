FROM python:3.12
LABEL authors="sinortax"

WORKDIR /app

COPY ./requirements.txt .
COPY ./.env .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./tracker .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
