FROM python:3.12-slim
WORKDIR /usr/src/app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt \
    && addgroup --system app \
    && adduser --system --ingroup app app

COPY app ./app
COPY frontend ./frontend

RUN chown -R app:app /usr/src/app
USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
