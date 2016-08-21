#!/usr/bin/env python3
import connexion
import datetime
import logging

from connexion import NoContent

# our memory-only api storage
APIS = {}


def get_apis(limit, api_type=None):
    return [api for api in APIS.values() if not api_type or api['api_type'] == api_type][:limit]


def get_api(api_id):
    api = APIS.get(api_id)
    return api or ('Not found', 404)


def put_api(api_id, api):
    exists = api_id in APIS
    api['id'] = api_id
    if exists:
        logging.info('Updating api %s..', api_id)
        APIS[api_id].update(api)
    else:
        logging.info('Creating api %s..', api_id)
        api['created'] = datetime.datetime.utcnow()
        APIS[api_id] = api
    return NoContent, (200 if exists else 201)


def delete_api(api_id):
    if api_id in APIS:
        logging.info('Deleting api %s..', api_id)
        del APIS[api_id]
        return NoContent, 204
    else:
        return NoContent, 404


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')