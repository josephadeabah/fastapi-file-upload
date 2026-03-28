FROM python:3.11-alpine

WORKDIR /app

# Alpine uses faster mirrors and smaller footprint
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/uploads

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]