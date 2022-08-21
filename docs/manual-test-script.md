# End-to-end test setup
- delete all but first model from file store
    https://console.cloud.google.com/storage/browser/swe-salary-predictor-store;tab=objects?forceOnBucketsSortingFiltering=false&project=swe-salary-predictor&prefix=&forceOnObjectsSortingFiltering=false

- delete last model (if not original model) reference from database
    ```sql
    DELETE FROM models_store WHERE uuid IN (SELECT uuid FROM models_store ORDER BY created_at DESC LIMIT 1) AND path != 'model_1656041268';
    ```

- delete all inputs from database
    ```sql
    TRUNCATE prediction_inputs;
    ```

- api call to update to refetch model (important to do after deleting reference in db)
    (DEV)  curl -X PUT http://localhost:8000/api/refetch-latest-model
    (PROD) curl -X PUT https://server-r4tqtdaqaq-uc.a.run.app/api/refetch-latest-model


# End-to-end test
- SEE: no inputs in database
- SEE: 1 model in google cloud store
- DO:  2 new inputs with save permission checked (remember input)
- SEE: predictions in webpage
- SEE: new inputs in database
- DO:  manually run retrainer
- SEE: new model in google cloud store
- SEE: "retreived 2 untrained input" in logs
- SEE: "Retrieved ref to latest model in db: {latest_model.path}" and "Loaded Model from file" in the logs
- DO:  enter another new input (same as before)
- SEE: different number than before