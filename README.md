[![codecov](https://codecov.io/gh/max-pfeiffer/device-statistics/graph/badge.svg?token=1jfd6K3L4s)](https://codecov.io/gh/max-pfeiffer/device-statistics)
# device-statistics

## Local Development
Create .env files in `config` directory according to the examples. Make sure to set `DATABASE_HOST=localhost` and
`API_DEVICE_REGISTRATION_BASE_URL=http://localhost:9000/device-registration/v1` to `localhost` when you want to run the
applications without docker compose.

Use the script `makejwt.sh` to create a JWT that you can use for local testing:
```shell
./makejwt.sh '{"iss": "https://auth.test.com", "scope": ["login", "statistics"]}'
```
Add contents of `public.pem` to IDP_PUBLIC_KEY in `device-statistics-app.env`.

Start the local Postgresql database with Docker compose:
```shell
docker compose up postgresql -d
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
Make sure to set `DATABASE_HOST=postgresql` to `postgresl` and
`API_DEVICE_REGISTRATION_BASE_URL=http://device-registration:9000/device-registration/v1` to `device-registration`
Run the whole stack with docker compose:
```shell
docker compose up -d
```
The handling of database migrations are controlled with these environment variables:
* DATABASE_ALEMBIC_MIGRATION_ROLLBACK
* DATABASE_ALEMBIC_MIGRATION_REVISION

If you want to rollback migrations to a certain revision, set the rollback to `true` and specify some migration revision. 
