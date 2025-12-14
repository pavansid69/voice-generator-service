FROM python:3.10-slim

# Install system deps
RUN apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI properly
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]