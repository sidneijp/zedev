# zedev

## URLs

- http://locahost:8000/api/ -> root REST API

## Dependencies

- docker >= 19.03
- docker-compose >= 1.25

## Quickstart

Build container's image:

```shell script
docker-compose build
```

Prepare environment:

```shell script
cp .env.sample .env
cp web/.env.sample web/.env
# edit .env and web/.env if necessary 
```

Run application services:

```shell script
docker-compose up
```

Run database migrations:

```shell script
docker-compose run --rm web src/manage.py migrate
```
```

## Running tests

Run:

```shell script
docker-compose run --rm web pytest --cov
```

Run on "watch mode" (rerun tests when a file changes):

```shell script
docker-compose run --rm web ptw -- --cov
```
