FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
COPY /docker.env /app/.env
RUN pip install --upgrade pip && pip install -r requirements.txt
# Copy the Django app code into the container
COPY /app/ /app/
# Expose port 8000 (adjust if your Django app runs on a different port)
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
