FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*



# Copy requirements first to leverage Docker cache
COPY setup.py .
COPY README.md .

# Install Python dependencies
RUN pip install -e .

# Copy application code
COPY . .

# Set Python path to include src directory
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Command to run the application
CMD ["python", "src/app.py"] 