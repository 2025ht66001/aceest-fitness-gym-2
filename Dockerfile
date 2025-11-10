# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# Install runtime deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

ENV PORT=8080
EXPOSE 8080

# Default: run Flask app
CMD ["python", "app.py"]
