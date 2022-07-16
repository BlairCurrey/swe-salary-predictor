#!/bin/bash

# parses .env-dev and sets as environment variables for alembic process.
# supports values with spaces and ignores commented (#) lines.
# https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs
env $(grep -v '^#' .env-prod | xargs -d '\n') alembic "$@"