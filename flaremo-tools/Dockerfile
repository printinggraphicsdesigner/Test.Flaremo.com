FROM python:3.11-slim

# LibreOffice + Bengali + Symbol support এর জন্য ভালো ফন্ট
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer \
    fonts-dejavu \
    fonts-noto-core \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-liberation \
    fonts-opensymbol \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "tools_hub.wsgi:application", "--bind", "0.0.0.0:10000"]
