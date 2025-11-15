# Using an image for dependency build stage which provides Poetry
# see: https://github.com/max-pfeiffer/python-poetry/blob/main/build/Dockerfile
FROM pfeiffermax/python-poetry:1.15.0-poetry2.1.1-python3.13.2-slim-bookworm as dependencies-build-stage
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR="/application_root/.cache" \
    PYTHONPATH=/application_root

# Set the WORKDIR to the application root.
# https://www.uvicorn.org/settings/#development
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR ${PYTHONPATH}

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY pyproject.toml ${PYTHONPATH}
#RUN poetry install --no-interaction --no-root --without=dev
RUN poetry install --no-interaction --no-root

# Using the standard Python image here to have the least possible image size
FROM python:3.13.9-slim-trixie as production-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    VIRTUAL_ENVIRONMENT_PATH="/application_root/.venv"

# Adding the virtual environment to PATH in order to "activate" it.
# https://docs.python.org/3/library/venv.html#how-venvs-work
ENV PATH="$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

# Principle of least privilege: create a new user for running the application
RUN groupadd -g 10001 python_application && \
    useradd -r -u 10001 -g python_application python_application

# Set the WORKDIR to the application root.
# https://www.uvicorn.org/settings/#development
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR ${PYTHONPATH}
RUN chown python_application:python_application ${PYTHONPATH}

# Copy virtual environment
COPY --from=dependencies-build-stage --chown=python_application:python_application ${VIRTUAL_ENVIRONMENT_PATH} ${VIRTUAL_ENVIRONMENT_PATH}

# Copy application files
COPY --chown=python_application:python_application /app ${PYTHONPATH}/app/

# Copy files for database migrations
COPY alembic.ini /${PYTHONPATH}/
COPY /alembic ${PYTHONPATH}/alembic

# Copy our custom entrypoint
COPY custom-entrypoint.sh /${PYTHONPATH}/

# Use the unpriveledged user to run the application
USER 10001
# Document the exposed port
EXPOSE 8000
# Run applications and database migration via a custom entrypoint
ENTRYPOINT ["/application_root/custom-entrypoint.sh"]