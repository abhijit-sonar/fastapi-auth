FROM python:3.8-alpine
WORKDIR /app


COPY Pipfile Pipfile.lock ./
COPY ./people_api ./people_api/

# Requird to build some dependencies
RUN apk add gcc musl-dev libffi-dev
RUN pip install pipenv
RUN pipenv install


CMD [ "pipenv", "run", "uvicorn", "people_api:app", "--host", "0.0.0.0", "--port", "8000"]
