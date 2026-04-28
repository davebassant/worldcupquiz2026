# Use Python 3.12 slim image for a lightweight footprint
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure the instance directory exists for SQLite
RUN mkdir -p instance

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "run.py"]
