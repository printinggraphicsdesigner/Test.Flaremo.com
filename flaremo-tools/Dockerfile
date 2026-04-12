FROM python:3.11-slim

# Minimal system dependencies for LibreOffice + Bengali font support
RUN apt-get update && apt-get install -y \
    libreoffice-writer \
    fonts-dejavu \
    fonts-noto-cjk \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "tools_hub.wsgi:application", "--bind", "0.0.0.0:10000"]
