# zedev

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/84409485c32544089086be4e94f9b6c2)](https://www.codacy.com/manual/sidneijp/zedev?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sidneijp/zedev&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/84409485c32544089086be4e94f9b6c2)](https://www.codacy.com/manual/sidneijp/zedev?utm_source=github.com&utm_medium=referral&utm_content=sidneijp/zedev&utm_campaign=Badge_Coverage)
[![CircleCI](https://circleci.com/gh/sidneijp/zedev.svg?style=shield)](https://app.circleci.com/pipelines/github/sidneijp/zedev)

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
