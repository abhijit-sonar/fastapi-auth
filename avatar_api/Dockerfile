FROM python:3.8-alpine
WORKDIR /app

COPY . .
RUN pip install pipenv
RUN pipenv install

CMD [ "pipenv", "run", "gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
