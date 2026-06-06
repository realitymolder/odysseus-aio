FROM docker:cli AS docker-cli
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

RUN pip install --no-cache-dir fastapi uvicorn jinja2

COPY aio/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY aio/start.sh /start.sh
COPY aio/app/ /app/

RUN chmod +x /start.sh

EXPOSE 9000
VOLUME ["/data"]

ENTRYPOINT ["/start.sh"]
