## Run with:  

    uvicorn main:app --reload

## Local env
python version 3.7.13

If getting an eror like:

    In file included from psycopg/psycopgmodule.c:28:0:
      ./psycopg/psycopg.h:35:10: fatal error: Python.h: No such file or directory
       #include <Python.h>

likely need to install:
    
    sudo apt-get install python3.7-dev


pip install tensorflow==2.8.0
pip install scikit-learn==1.0.2
pip install pandas==1.3.5
pip install psycopg2==2.9.3
pip install SQLAlchemy==1.4.37
pip install fastapi[all]