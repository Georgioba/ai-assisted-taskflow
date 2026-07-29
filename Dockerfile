FROM python:3.12-slim AS base
WORKDIR /usr/src/app

RUN python -m pip install --no-cache-dir fastapi uvicorn pydantic

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
