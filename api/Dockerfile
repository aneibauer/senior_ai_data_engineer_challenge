FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary pydantic databases[postgresql] asyncpg

ENV PYTHONPATH=/app:/app/api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]