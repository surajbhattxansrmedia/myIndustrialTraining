FROM python:3.11.4-slim-bullseye

RUN pip install poetry==1.8.2

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --only main

COPY . .

# Debug: List installed packages (remove after confirming)
RUN python -m pip list

CMD ["python", "-m", "uvicorn", "playground_fantasymanager.web.application:get_app", "--host", "0.0.0.0", "--port", "8000"]