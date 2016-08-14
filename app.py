#!/usr/bin/env python3
import connexion
from connexion import NoContent
import datetime
import logging
from gcloud import datastore
import json

# our memory-only api storage
def Json(api):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {id: id, prop: val, ...}
    """
    if not api:
        return None
    j = {'id': api['id'], 
        'name': api['name'],
        'api_type': api['api_type'],
    }
    return api

def get_client():
    return datastore.Client('lithe-strata-123819')

def get_apis(api_type=None):
    ds = get_client()
    query = ds.query(kind='API', order=['name'])
    if (api_type != None): query.where('api_type ==',api_type)
    prepJson = []
    apis = query.fetch()
    for a in apis:
        prepJson.append(Json(a))

    return prepJson

def get_api(api_id):
    ds = get_client()
    key = ds.key('API', api_id)
    entity = ds.get(key)
    exists = (entity != None)
    if exists:
        return Json(entity)
    else: 
        return ('Not found', 404)


def put_api(api_id, api):
    ds = get_client()
    key = ds.key('API', api_id)
    entity = ds.get(key)
    exists = (entity != None)
    api['id'] = api_id
    if exists:
        logging.info('Updating api %s..', api_id)
        api['updated'] = datetime.datetime.utcnow()
    else:
        logging.info('Creating api %s..', api_id)
        entity = datastore.Entity(key=key)
        api['created'] = datetime.datetime.utcnow()

    entity.update(Json(api))
    ds.put(entity)   
    return NoContent, (200 if exists else 201)

def delete_api(api_id):
    ds = get_client()
    key = ds.key('API', api_id)
    entity = ds.get(key)
    exists = (entity != None)
    if exists:
        logging.info('Deleting api %s..', api_id)
        ds.delete(key)
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
