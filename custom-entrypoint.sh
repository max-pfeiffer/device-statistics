#!/usr/bin/env bash


case ${1} in
  device-statistics)
    cd "$PYTHONPATH" || return 100
    uvicorn app.device_statistics.main:app --host 0.0.0.0 --port "$UVICORN_PORT" || return $?
    ;;

  device-registration)
    cd "$PYTHONPATH" || return 100
    uvicorn app.device_registration.main:app --host 0.0.0.0 --port "$UVICORN_PORT" || return $?
    ;;

  database-migrations)
    cd "$PYTHONPATH" || return 100
    if [ "$DATABASE_ALEMBIC_MIGRATION_ROLLBACK" = "true" ]; then
      alembic downgrade "$DATABASE_ALEMBIC_MIGRATION_REVISION" || return $?
    else
      alembic upgrade head || return $?
      alembic check || return $?
    fi
    ;;

  *)
    return 104
    ;;
esac
