FROM python:3.10-alpine

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && \
    chmod +x entrypoint.sh

ENV HTTP_PORT=8081
ENTRYPOINT ["./entrypoint.sh"]
