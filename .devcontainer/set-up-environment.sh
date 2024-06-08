#!/usr/bin/env bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

PGPASSWORD=postgres psql -h localhost postgres -U postgres < databases/create_databases.sql
alembic upgrade head
DATABASE_URL="postgresql://localhost:5432/ai_starter_test?user=ai_starter&password=ai_starter" alembic upgrade head
