FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir google-adk toolbox-core
COPY . .
CMD ["sh", "-c", "adk web --host 0.0.0.0 --port ${PORT:-8080} ."]
