# Run with:  

    uvicorn main:app --reload

# Local env
python version 3.7.13

If getting an eror like:

    In file included from psycopg/psycopgmodule.c:28:0:
      ./psycopg/psycopg.h:35:10: fatal error: Python.h: No such file or directory
       #include <Python.h>

likely need to install:
    
    sudo apt-get install python3.7-dev

# Deployment
I am deploying via gcloud cli on my local system via `source ./build-and-deploy.sh`.

The `service.yaml` file holds the configuration for the service. Current config can be pulled in with:

    gcloud run services describe server --format export > service.yaml

if changing the service.yaml configuration, run this to update:

    gcloud run services replace service.yaml

note, may need to remove 'spec.template.metadata.name' before replacing yaml, per this SO post https://stackoverflow.com/questions/70311143/deploying-cloud-run-via-yaml-gives-revision-named-yourservicename-00001-soj-wi

## secrets and env vars in production
`service.yaml` sets environment vars and references secrets that are stored in google cloud secret manager. The following env vars are used in production and set as secrets in google cloud:

DB_SOCKET_DIR
INSTANCE_CONNECTION_NAME (from cloud sql)
GOOGLE_APPLICATION_CREDENTIALS (reference to cloud store json file location. should be included in dockerfile)

Additionally, we directly set non-sensitive env vars in `service.yaml`, such as:

TF_CPP_MIN_LOG_LEVEL=2

Since we are using google cloud sql, cloud run is able to locate the db via some internal files, so it does not need the host in prod.