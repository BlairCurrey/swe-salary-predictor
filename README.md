# swe-salary-predictor
A salary predictor for software engineers. Powered by a machine learning model that updates with your input.

##  Repo Overview:

## docs
Miscellaneous documentation

## analytics
Python environment for bulding and testing the model for predicting salaries.

## server
Fastapi server that will store user input into db, get latest model from db, predict salaries using model, and serve results to the users in jinja2 templates.

## database
Postgres database initialized with docker and managed with `alembic`.

## retrainer
Takes the original model and fits additional data to it. Saves the resulting model.