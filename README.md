[![codecov](https://codecov.io/gh/max-pfeiffer/device-statistics/graph/badge.svg?token=1jfd6K3L4s)](https://codecov.io/gh/max-pfeiffer/device-statistics)
# device-statistics

## Local Development
Create .env files in `config` directory according to the examples. Use the script `makejwt.sh` to create a JWT
that you can use for local testing. Add contents of `public.pem` to IDP_PUBLIC_KEY in `device-statistics-app.env`.

Start the local Postgresql database with Docker compose:
```shell
docker compose up -d
```
Apply database migrations with alembic:
```shell
alembic upgrade head
```
Create new database migrations with alembic:
```shell
alembic revision --autogenerate -m "meaningful description"
```
Add a Pycharm run configuration or start Uvicorn manually. For `device-statistics` app:
```shell
uvicorn --reload --env-file config/device-statistics-app.env --port 8000
```
For `device-registration` app:
```shell
uvicorn --reload --env-file config/device-registration-app.env --port 9000
```

## Local Testing
