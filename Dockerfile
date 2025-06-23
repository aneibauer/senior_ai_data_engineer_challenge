# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your code into the container, into /app specifically
COPY . .

# Default command to run (can be overridden in docker-compose)
# CMD ["python3", "-m", "scripts.stream_processor"]