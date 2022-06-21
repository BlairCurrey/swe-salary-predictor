# local dev setup 
`libpq-dev` is a system dependancies for the python pacakge `psycopg2` (the psql python driver). Install that before installing the python packages.

on ubuntu:

    sudo apt-get install libpq-dev

Create/run db via docker:

    docker-compose up -d

Access locally via shell:

    docker exec -it database_database_1 bash
    su postgres
    psql swe_salary_estimator

# migrations

alembic is used for database migrations. General usage instructions can be found in these docs: https://alembic.sqlalchemy.org/en/latest/tutorial.html

The connection to postgres is handled via a url in `./alembic.ini`.

To make a new migration:

    alembic revision -m "create prediction_inputs table"

This creates a new migration script under `alembic/versions`.

To upgrade to most recent version:

    alembic upgrade head

Could alternatively replace head with revision id to upgrade to a specific revision instead.

To undo the last migration:

    alembic downgrade -1
