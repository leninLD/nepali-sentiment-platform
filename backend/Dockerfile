FROM python:3.11-slim

WORKDIR /app

# Install system dependencies: Chromium/chromedriver for Selenium, fonts for wordcloud
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONPATH=/app
ENV MPLBACKEND=Agg
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and scripts
COPY ./app /app/app
COPY ./scripts /app/scripts

# Create model directory (model will be downloaded at runtime if not present)
RUN mkdir -p /app/model

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8000}/api/v1/health').read()" || exit 1

# Start uvicorn, binding to $PORT (set by Render) or default to 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

