#!/usr/bin/env bash

UVICORN_PORT=${2:-"8000"}

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
    if [ "$DATABASE_ROLLBACK" = "true" ]; then
      alembic downgrade -1 || return $?
    else
      alembic upgrade head || return $?
      alembic check || return $?
    fi
    ;;

  *)
    return 104
    ;;
esac
