# Use an official Python runtime. Using 3.12 to match your environment.
FROM python:3.12-slim

# Set environment variables to prevent .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Upgrade pip and install all dependencies from requirements.txt
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This copies your 'app/' directory, 'alembic~/' directory, etc.
COPY . .

# Expose the port that Hugging Face Spaces expects
EXPOSE 7860

# Command to run the application
# Binds to all interfaces (0.0.0.0) and the required port (7860)
# Assumes your 'alembic upgrade head' was run locally on your Neon DB
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]