[![codecov](https://codecov.io/gh/max-pfeiffer/device-statistics/graph/badge.svg?token=1jfd6K3L4s)](https://codecov.io/gh/max-pfeiffer/device-statistics)
# device-statistics


## Quick start
Create .env files in `config` directory according to the examples i.e.,
```shell
cp db.env.example db.env 
```
Use the script `makejwt.sh` to create a JWT with scopes that you can use for local testing:
```shell
./makejwt.sh '{"iss": "https://auth.test.com", "scope": ["login", "statistics"]}'
```
Add contents of `public.pem` to `IDP_PUBLIC_KEY` in `device-statistics-app.env`.
```shell
docker compose up -d
```
As soon as images are built and all containers are up and running, the APIs are available on:
* http://127.0.0.1:8000/device-statistics/docs
* http://127.0.0.1:9000/device-registration/docs

You can use the autodocs to issue requests. Use the `Authorize` button for device statistics API to authenticate with
the JWT you created earlier.

The handling of database migrations is controlled with these environment variables:
* DATABASE_ALEMBIC_MIGRATION_ROLLBACK
* DATABASE_ALEMBIC_MIGRATION_REVISION

If you want to rollback migrations to a certain revision, set the rollback to `true` and specify some migration
revision in `db-alembic.env`.

## Local Development
Setup a virtual environment and install dependencies with [Poetry](https://python-poetry.org/):
```shell
poetry install --no-root
```

Modify the .env files in `config` directory You created earlier:
* set `DATABASE_HOST=localhost`
* set `API_DEVICE_REGISTRATION_BASE_URL=http://localhost:9000/device-registration/v1`

Both environment variables need to point to localhost as you are not using the internal Docker network more.  

Start the local Postgresql database with Docker compose:
```shell
docker compose up postgresql -d
```

### Configure IDE
Add a Pycharm run configuration or start Uvicorn manually. For `device-statistics` app:
```shell
uvicorn --reload --env-file config/device-statistics-app.env --port 8000
```
For `device-registration` app:
```shell
uvicorn --reload --env-file config/device-registration-app.env --port 9000
```

### Apply and generate database migrations
Apply database migrations with alembic:
```shell
alembic upgrade head
```
Create new database migrations with alembic:
```shell
alembic revision --autogenerate -m "meaningful description"
```
