# API Registry for App Engine

This app engine implements a REST service using the `Connexion`_ Python library for 
registering APIs with the API portal.

Connexion is a framework on top of Flask_ to automagically handle your REST API requests
based on `Swagger 2.0 Specification`_ files in YAML.

## Features

* bundled Swagger UI (served on `/ui/`_ path)
* API registry service on /apis, /api/{api_id}

## Prerequisites

* `Python 3`
* `git`

## Files

The example application only needs very few files:

* ``swagger.yaml``: the API Registry REST API Swagger definition
* ``app.py``: implementation of the pet shop operations with in-memory storage
* ``requirements.txt``: list of required Python libraries
* ``Dockerfile``: to build the example as a runnable Docker image

## Running Locally

You can run the Python application directly on your local operating system:

```
    $ git clone http://www.github.com/bgillock/api-registry
    $ cd api-registry
    $ sudo pip3 install -r requirements.txt
    $ ./app.py # start the HTTP server
```

Visit http://localhost:8080/ui/ to see the API documentation.
Go to PUT api/{api_id} and `try it out`. This will register an API.

## Deploying to App Engine

To deploy to App Engine you will need to install Google Cloud SDK.

```
    $ git clone http://www.github.com/bgillock/api-registry
    $ cd api-registry
    $ gcloud init <- Select your account name and project
    $ gcloud auth login
    $ gcloud app deploy
```
    


