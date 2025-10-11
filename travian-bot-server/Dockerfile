# Use official Python 3.12 slim image
FROM python:3.12-slim

# --- Install system dependencies ---
RUN apt-get update && apt-get install -y \
    chromium \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for headless Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/bin/chromium

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy bot source code
COPY . .

# Expose API port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

