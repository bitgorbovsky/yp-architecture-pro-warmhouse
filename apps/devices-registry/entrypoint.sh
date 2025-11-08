#!/usr/bin/env sh

exec uvicorn service.main:app --host 0.0.0.0 --port $HTTP_PORT
