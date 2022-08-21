export PROJECT_ID=swe-salary-predictor
export REGION=us-central1
export CONNECTION_NAME=swe-salary-predictor:us-central1:postgres-db

gcloud builds submit \
  --tag gcr.io/$PROJECT_ID/server \
  --project $PROJECT_ID

gcloud run deploy server \
  --image gcr.io/$PROJECT_ID/server \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNECTION_NAME \
  --project $PROJECT_ID
  # TODO: specify max instances of 1 (was already configured in gc site)