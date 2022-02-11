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
