# retrainer
The retrainer pulls untrained inputs from the database and fits them to our existing model. It will save the new model in the filestore and update the database with a reference to this file, as well as mark the inputs as trained.

# local dev
After installing the dependencies we change directories to `./src` and run `dev_run.py` to run the retrainer. `dev_run.py` It will connect to the database and filestore according to credentials in the `.env`. The google cloude filestore json credential file will need to be stored locally.

## deployment
The retrainer script is deployed as google cloud function. This can be deployed with `./deploy.sh`. This script will set the required environment variables from `.env-prod`.

The retrainer function works in conjunction with a `retrain-model` Pub/Sub topic created on the Google Cloud console. A cloud schedule task was setup to publish a message to this topic periodically which will trigger the retrainer. Google Functions dictates the name and arguments of the retrainer function in `src/main.py`.
