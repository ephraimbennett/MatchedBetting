# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

ENV HOST=0.0.0.0

# Copy the requirements file into the container
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright?
RUN playwright install --with-deps

# Copy the rest of the application code
COPY . .

# Collect static files into STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
