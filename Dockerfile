FROM python:3.11-bullseye
COPY . /usr/src/app
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR /usr/src/app
RUN poetry install