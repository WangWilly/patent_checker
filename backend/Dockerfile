################################################################################
# Base image
FROM python:3.12.7-bookworm as python

ENV PYTHONUNBUFFERED=true

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

################################################################################
# Install poetry
FROM python as pypoetry
RUN apt update && apt install -y cmake

RUN curl -sSL https://install.python-poetry.org | python3 -

################################################################################
# Install runner dependencies
FROM pypoetry as runner-deps

COPY ./backend/poetry.lock ./backend/pyproject.toml ./

RUN poetry install --without dev --no-interaction --no-ansi -vvv

################################################################################
# Copy the dependencies to the final image
FROM python as runner

ENV PYTHONPATH="/app"

COPY --from=runner-deps /app /app
COPY ./scripts/serve-backend.sh /app/entrypoint.sh
COPY ./backend ./

ENTRYPOINT ["/app/entrypoint.sh"]
