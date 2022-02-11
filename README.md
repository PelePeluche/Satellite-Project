# Presentation

This repository contains all the files needed to execute my resolution to the **imagine** challenge for the _cohorte 2022_ (_link_ to the challenge https://imaginefellowships.com/product-cohorts/march-2022-cohort/product-lab-project-statement).

# Files

- `main.py` : Has the two endpoints created. Even though the tagline had three endpoints, I thought it was better not to create an extra endpoint to filter a resource by name, but to implement the filter in the same endpoint.
- `models.py` : It contains the declaration of the two classes used in the project and the lines of code necessary for these classes to be mapped to the database and their tables to be created.
- `service.py` : It contains all the functions that are required for the endpoints implemented in `main.py`, as well as a function that serves to load the data in the `starlink.py` module to the database.
- `starlink.py` : It contains the data in the proper format to be loaded into the database. In this file all values declared as _null_ were changed to _None_.
- `test.py` : This file contains the tests implemented for the different functionalities of the different modules.
- `requirements.txt` : It contains a list of the dependencies needed to run the project and their versions.

# Instructions for using the APIs

## Install the virtual environment

- Create a new environment with `virtualenv`

  > virtualenv env

- Activate the virtual environment

  - Linux

    > source env/bin/activate

  - Windows

    > source env/Scripts/activate

- Install dependencies

  > pip install -r requirements.txt

## Start server

- To activate the virtual environment

  > source env/Scripts/activate

- To start the server locally

  > uvicorn main:app --reload

## Loading database

- From the Python console import the function data_loading from the module service.py

  > from service import data_loading

- From the Python console call the data_loading function to create the database

  > data_loading()

## To run the tests

- From the Python console run the command

  > pytest test.py

## To see documentation

- Start the server

  > uvicorn main:app --reload

- Go to the link

  > http://localhost:8000/docs#/
