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
COPY . .

# Expose port
EXPOSE 8080

# Start the Flask app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app.app:app"]
