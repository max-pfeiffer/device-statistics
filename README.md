# device-statistics

## Local Development
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
