Flask-Elasticsearch
=============

Simple Flask extension that allows to access Elasticsearch in your Flask application.

[Elasticseach](https://elasticsearch-py.readthedocs.io)

[Elasticseach DSL](https://elasticsearch-dsl.readthedocs.io)

[Flask Extensions](https://flask.palletsprojects.com/en/1.1.x/extensiondev/)

Installation
------------

To install it, simply:

    pip install Flask-Elasticsearch

Usage
-----

You only need to import and initialize your app

    from flask import Flask
    from flask_elasticsearch import Elasticsearch

    app = Flask(__name__)
    app.config['ELASTICSEARCH_HOST']  = 'http://localhost:9200'
    elasticsearch = Elasticsearch(app)

Health Check
------------

es.cluster.health(wait_for_status='yellow', request_timeout=1)

Storage
------------

    from elasticsearch_dsl import Document, Integer, Keyword

    class DatasetRow(Document):
      dataset = Keyword()
      id = Integer()
      built_form_key = Keyword()

    DatasetRow(dataset='/ns/dataset/key', id=1, built_form_key='bt__duplex').save()
    DatasetRow(dataset='/ns/dataset/key', id=2, built_form_key='bt__hospital').save()

Query
------------

    from elasticsearch_dsl import Search

    response = (
      Search(index='dataset')
      .filter('term', built_form_key='bt__duplex')
      .execute())

    for row in response:
      print(row.id)
