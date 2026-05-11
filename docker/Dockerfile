# Use lightweight Python image
FROM python:3.9-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]