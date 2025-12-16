# Use Python 3.13 slim image
FROM python:3.13-slim

# Install build tools and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency file first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app /app/

# Expose port
EXPOSE 8080

# Run the app
CMD ["python", "/app/main.py"]