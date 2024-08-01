# Stage 1: Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy only necessary files from the build stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Add application code
COPY . .

EXPOSE 3000

# Command to run the application
CMD ["python", "app.py"]
