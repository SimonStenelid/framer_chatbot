# Use Python 3.11 as the base image (slim version for smaller size)
FROM python:3.11-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file first (this helps with Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from your project to the container
COPY . .

# Expose port 7860 (Hugging Face Spaces uses this port)
EXPOSE 7860

# Command to run when the container starts
# Using gunicorn (production-ready web server) instead of Flask's dev server
CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "app:app"]
