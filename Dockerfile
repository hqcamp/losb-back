FROM python:3.12

RUN pip install --upgrade pip \
    && pip install poetry

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY ./app /app

ENV SERVICE_HOST="0.0.0.0" \
    SERVICE_PORT=8080

CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --workers=1 --access-logfile - --error-logfile - --bind $SERVICE_HOST:$SERVICE_PORT  app.wsgi

EXPOSE 8080
