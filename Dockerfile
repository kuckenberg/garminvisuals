FROM python:3.12-slim

WORKDIR /app

COPY . /app
COPY crontab.txt /etc/cron.d/garmin-cron

RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update && apt-get install -y cron \
    && rm -rf /var/lib/apt/lists/*
RUN chmod 0644 /etc/cron.d/garmin-cron

RUN crontab /etc/cron.d/garmin-cron

CMD ["cron", "-f"]