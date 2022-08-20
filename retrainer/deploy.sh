#!/bin/bash

# bundle code and requirements into ./target
cp -rT ./src ./target # resursive, override existing ./target
cp ./requirements.txt ./target

env_vars=$(grep -v '^#'  .env-prod | tr '\n' ',' | xargs -d '\n')

gcloud functions deploy retrainer \
    --runtime python37 \
    --trigger-topic="retrain-model" \
    --set-env-vars $env_vars \
    --source ./target \
    --memory 1024MB \
    --timeout 540s