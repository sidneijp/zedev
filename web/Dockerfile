FROM python:3.8

RUN apt update && apt upgrade -y

RUN pip install --no-cache-dir pipenv pip setuptools -U

RUN apt install -y libpq-dev build-essential ca-certificates libgeos-dev libproj-dev libgdal-dev

WORKDIR /code

COPY Pipfile Pipfile.lock ./

RUN mkdir -p .venv && \
    export PIP_NO_CACHE_DIR=false && \
    pipenv install --dev

COPY . .

RUN export PIP_NO_CACHE_DIR=false && \
    pipenv run pip install -e .

ENTRYPOINT ["pipenv", "run"]

CMD ["gunicorn", "--pythonpath", "src", "-b", "0.0.0.0:8000", "-w", "4", "--reload", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "debug", "main.wsgi"]
