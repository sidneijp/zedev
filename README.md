# zedev

[![Codacy Code Quality Badge](https://app.codacy.com/project/badge/Grade/84409485c32544089086be4e94f9b6c2)](https://www.codacy.com/manual/sidneijp/zedev?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sidneijp/zedev&amp;utm_campaign=Badge_Grade)
[![Codacy Coverage Badge](https://app.codacy.com/project/badge/Coverage/84409485c32544089086be4e94f9b6c2)](https://www.codacy.com/manual/sidneijp/zedev?utm_source=github.com&utm_medium=referral&utm_content=sidneijp/zedev&utm_campaign=Badge_Coverage)
[![CircleCI](https://circleci.com/gh/sidneijp/zedev.svg?style=shield)](https://app.circleci.com/pipelines/github/sidneijp/zedev)

## URLs

- [Challenge Description](https://github.com/ZXVentures/ze-code-challenges/blob/master/backend.md)
- [Root REST API - local](http://0.0.0.0:8000/api/)
- [Docker image on Docker Hub](https://hub.docker.com/repository/docker/sidneijp/zedev)
- [Codacy's analysis](https://app.codacy.com/gh/sidneijp/zedev/dashboard?branch=master)
- [GitHub repository](https://github.com/sidneijp/zedev)
- [CircleCI pipelines](https://app.circleci.com/pipelines/github/sidneijp/zedev)

## Dependencies

- [docker](https://docs.docker.com/engine/install/) >= 19.03
- [docker-compose](https://docs.docker.com/compose/install/) >= 1.25

## Quickstart

Prepare environment:

```shell script
cp .env.sample .env
cp web/.env.sample web/.env
# edit .env and web/.env if necessary 
```

Build container's image:

```shell script
docker-compose build
```

Run application services:

```shell script
docker-compose up
```

Run database migrations:

```shell script
docker-compose run --rm web src/manage.py migrate
```

## Usage

After the project is up and running try some API calls:

- Create a partner:

```shell script
curl -X POST 'http://0.0.0.0:8000/api/partners/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "tradingName": "Adega da Cerveja - Pinheiros",
  "ownerName": "Zé da Silva",
  "document": "51321238910001",
  "coverageArea": {
    "type": "MultiPolygon",
    "coordinates": [
      [[[30, 20], [45, 40], [10, 40], [30, 20]]],
      [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
    ]
  },
  "address": {
    "type": "Point",
    "coordinates": [-47.57421, -21.785741]
  }
}'
```

- Retrieve it by it's id:

```shell script
curl -X GET 'http://0.0.0.0:8000/api/partners/1/' --header 'Content-Type: application/json'
```

- Try to create more partners then list them all:

``` shell script
curl -X GET 'http://0.0.0.0:8000/api/partners/' --header 'Content-Type: application/json'
```

- You can also list them filtering by those who cover a certain coordinate:

``` shell script
curl -G -X GET 'http://0.0.0.0:8000/api/partners/' --data-urlencode 'address={"type": "Point", "coordinates": [15, 10]}' --header 'Content-Type: application/json'
```
* in this case, lat=15, long=10

- To get the nearest partner that cover a coordinate, use:

```shell script
curl -X GET 'http://0.0.0.0:8000/api/partners/15,10/nearest/' --header 'Content-Type: application/json'
```

* in this case, lat=15, long=10

## Deploy to production environment

The aplication uses docker to run so it can run in any platform that supports it or you can install docker deamon in the production host an run it.

## Running tests

Run:

```shell script
docker-compose run --rm web pytest --cov
```

Run on "watch mode" (rerun tests when a file changes):

```shell script
docker-compose run --rm web ptw -- --cov
```
