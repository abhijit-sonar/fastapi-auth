FROM python:3.8-alpine
WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install

COPY ./people_api ./people_api/

CMD [ "pipenv", "run", "uvicorn", "people_api:app", "--host", "0.0.0.0", "--port", "8000"]

