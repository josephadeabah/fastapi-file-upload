FROM python:3.11-slim

WORKDIR /app

# Fix Debian repo mirror (important)
RUN sed -i 's/deb.debian.org/mirror.math.princeton.edu/g' /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy project files
COPY . .

# Create uploads folder
RUN mkdir -p /app/uploads

# Copy wait script
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

EXPOSE 8000

CMD ["/wait-for-db.sh"]