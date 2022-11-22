FROM python:3.10-bullseye

ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/.cache

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:${POETRY_HOME}/venv/bin"

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml README.md ./

COPY docker_config.toml ./config.toml

COPY modula_modbus/ ./modula_modbus/

RUN ["poetry", "install"]

CMD ["poetry","run", "python", "-m", "modula_modbus"]

