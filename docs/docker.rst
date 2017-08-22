Local Docker Development Instructions
=====================================


Mac-specific
------------

Install `Docker for Mac <https://www.docker.com/docker-mac>`_ .


Initial Local Development Setup
-------------------------------

Configure environment to use docker settings file::

  echo "DJANGO_SETTINGS_MODULE=eatsmart.settings.docker" > .env

Build the containers::

  docker-compose build

Bring up the containers in this order (any way around this to avoid errors?)::

  docker-compose up -d db
  docker-compose up -d app

Now visit http://localhost:8000 in your browser.


Load DB Dump
~~~~~~~~~~~~

The easiest way to get data is to load a db dump::

  wget https://s3.amazonaws.com/ncfoodinspector/eatsmart.tar.zip
  unzip eatsmart.tar.zip
  docker exec -i "`docker-compose ps -q db`" pg_restore --data-only --clean --no-acl --no-owner -U "postgres" -d "postgres" < eatsmart.tar

You'll see a few errors for ``auth_permission``, ``django_content_type``, and ``django_migrations`` tables, but it will still work.

  .. docker-compose run app /venv/bin/python manage.py migrate
