# local dev setup 
`libpq-dev` is a system dependancies for the python pacakge `psycopg2` (the psql python driver). Install that before installing the python packages.

on ubuntu:

    sudo apt-get install libpq-dev

Setup environment variabels with local db credentals. See .env-example

Create/run db via docker:

    docker-compose up -d

Access locally via shell:

    docker exec -it database_database_1 bash
    su postgres
    psql swe_salary_estimator

# migrations

alembic is used for database migrations. General usage instructions can be found in these docs: https://alembic.sqlalchemy.org/en/latest/tutorial.html. Ensure the .env has the correct credentials (local vs prod).

The connection to postgres is handled via a url in `./alembic.ini`.

To make a new migration:

    alembic revision -m "create prediction_inputs table"

This creates a new migration script under `alembic/versions`.

To upgrade to most recent version:

    alembic upgrade head

Could alternatively replace head with revision id to upgrade to a specific revision instead.

To undo the last migration:

    alembic downgrade -1

# deployment

## previous instructions, for heroku
_moved off heroku because rotating credentials were too hard to manage outside of heroku environment_
The database is hosted on heroku. Install the heroku cli: https://devcenter.heroku.com/articles/heroku-cli

Credentials (including database name) are generated when the service is provisioned and change periodically. To interface with the db via alembic, change the `.env` to use credentials found on heroku for the `swe-salar-predictor` project. These need to be manually set for now. Once set, alembic can be run against the prod db from your local system.

## connecting to google cloud sql from local machine
https://cloud.google.com/sql/docs/postgres/connect-admin-ip

Must whitelist local IP address in google cloud sql. 

Use the `./scripts/alembic_prod.sh` wrapper to use alembic with production db. This script just wraps the `alembic` command with production env vars (to be defined in a `.env-prod` file). Try `./alembic_prod.sh current` to test connection to database.

connect to prod db via shell with local postgres client using `./scripts/psql_prod.sh` which also references the same `.env-prod` file.