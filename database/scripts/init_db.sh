#!/bin/bash
# used by docker-compose
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE swe_salary_estimator;
EOSQL