FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install sqlite-vss
RUN git clone https://github.com/asg017/sqlite-vss.git \
    && cd sqlite-vss \
    && make loadable \
    && cp dist/debug/vss0.so /usr/local/lib/sqlite_vss0.so \
    && cd .. \
    && rm -rf sqlite-vss

# Copy requirements first to leverage Docker cache
COPY setup.py .
COPY README.md .

# Install Python dependencies
RUN pip install -e .

# Copy application code
COPY . .

# Command to run the application
CMD ["python", "app.py"] 