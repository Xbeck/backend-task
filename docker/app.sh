#!/bin/bash

# alembic downgrade -1

alembic upgrade head

gunicorn src.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000