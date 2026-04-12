FROM python:3.11-slim

# Minimal LibreOffice for Word → PDF (headless)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer \
    fonts-dejavu \
    fonts-noto-cjk \
    fonts-liberation \
    fonts-opensymbol \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "tools_hub.wsgi:application", "--bind", "0.0.0.0:10000"]
