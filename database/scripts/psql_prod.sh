#!/bin/bash

env_vars=$(grep -v '^#' .env-prod | xargs -d '\n')
PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER $DB_NAME