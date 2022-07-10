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