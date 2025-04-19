#!/bin/bash

echo "Waiting for PostgreSQL..."
sleep 10

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 