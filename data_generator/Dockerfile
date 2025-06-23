# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements_2.txt .
RUN pip install --upgrade pip && pip install -r requirements_2.txt

# Copy the rest of your code into the container
COPY . .

# Default command to run (can be overridden in docker-compose)
CMD ["python3", "-m", "stream_processor"]