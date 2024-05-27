FROM python:3.9-slim

WORKDIR /app/judge_service

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    openjdk-11-jdk && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "app.py"]