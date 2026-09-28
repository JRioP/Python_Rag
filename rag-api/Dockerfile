FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    FASTEMBED_CACHE=/app/models \
    ANONYMIZED_TELEMETRY=False
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Bake the vector DB and the embedding model into the image so wake-ups are faster
RUN python ingest.py
# Render provides $PORT (default 10000); listen on 0.0.0.0
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}
