# --- Base image ---
FROM python:3.13-slim

# --- Environment variables ---
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# --- Install system dependencies ---
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome as default for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# --- Set working directory ---
WORKDIR /app

# --- Copy project files ---
COPY . /app

# --- Install Python dependencies ---
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# --- Expose port ---
EXPOSE 8000

# --- Run FastAPI server ---
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
