# Use the official Python image
FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app

# Expose port 5000 for Flask
EXPOSE 5000

# Run Flask with debug enabled
CMD ["python", "app.py"]
