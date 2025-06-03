FROM python:3.11.4-slim-bullseye

RUN pip install poetry==1.8.2

WORKDIR /app

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --only main

# Now copy the rest of the code
COPY . .

CMD ["python", "-m", "uvicorn", "playground_fantasymanager.web.application:get_app", "--host", "0.0.0.0", "--port", "8000"]