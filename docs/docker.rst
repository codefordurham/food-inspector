Local Docker Development Instructions
=====================================


Mac-specific
------------

Install `Docker for Mac <https://www.docker.com/docker-mac>`_ .


Initial Local Development Setup
-------------------------------

Checkout the code repository::

  git clone git@github.com:codefordurham/food-inspector.git
  cd food-inspector/

The default development environment will provide you with running PostgreSQL and Django containers:

* PostgreSQL: v9.3 w/ PostGIS v2.3. ``./pgdata`` is mounted from the host environment to persist data.
* Django: Mounts the current directory into the container and uses ``manage.py runserver``.

The configuration is loaded from ``docker-compose.override.yml`` and ``docker-compose.yml``, respectively.

Configure environment to use the docker settings file::

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

  curl -O https://s3.amazonaws.com/ncfoodinspector/ncfoodinspector.dump.zip
  unzip ncfoodinspector.dump.zip
  docker exec -i "`docker-compose ps -q db`" pg_restore --data-only --no-acl --no-owner -U "postgres" -d "postgres" < db.dump

You'll see a few errors for ``auth_permission``, ``django_content_type``, and ``django_migrations`` tables, but it will still work.

If you've modified the DB locally and want a fresh start, follow these steps first::

  docker-compose down
  docker volume rm -rf ./pgdata  # remove existing PostgreSQL data
  docker-compose up -d db  # wait 5-10 seconds after running this
  docker-compose up -d app  # this will run manage.py migrate and provide a fresh DB
