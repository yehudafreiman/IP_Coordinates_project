FROM python:3.11-slim

WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ ./

# Expose the port
EXPOSE 8001

# Run the application
CMD ["python", "main.py"]