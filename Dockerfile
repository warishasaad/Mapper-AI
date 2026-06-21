# Dockerfile

# Use an official Python runtime as a parent image.
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for OCR (pytesseract) and OpenCV
# THIS MUST BE DONE AS ROOT - BEFORE switching users
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies (also as root)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copy all your application code into the container (as root)
COPY . /app

# NOW create a non-root user and change ownership of the app directory
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

# Switch to the non-root user for running the application
USER appuser

# Expose the ports the services will run on
EXPOSE 8000
EXPOSE 8501