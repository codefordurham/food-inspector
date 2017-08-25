Local Docker Development Instructions
=====================================


Mac-specific
------------

Install `Docker for Mac <https://www.docker.com/docker-mac>`_ .


Initial Local Development Setup
-------------------------------

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

  wget https://s3.amazonaws.com/ncfoodinspector/eatsmart.tar.zip
  unzip eatsmart.tar.zip
  docker exec -i "`docker-compose ps -q db`" pg_restore --data-only --clean --no-acl --no-owner -U "postgres" -d "postgres" < eatsmart.tar

You'll see a few errors for ``auth_permission``, ``django_content_type``, and ``django_migrations`` tables, but it will still work.


Deploy Setup
------------

This environment will provide you with PostgreSQL, RabbitMQ, Celery, and Django containers. The configuration is loaded from ``docker-compose.dev.yml`` and ``docker-compose.yml``, respectively.

Create environment variables in ``.env``::

  DJANGO_SETTINGS_MODULE=eatsmart.settings.deploy
  ENVIRONMENT=LOCAL  # LOCAL = testing production env with compose
  SECRET_KEY=<fill-me-in>
  DOMAIN=localhost
  DATABASE_URL=postgis://postgres:postgres@db:5432/postgres
  RABBITMQ_DEFAULT_USER=admin
  RABBITMQ_DEFAULT_PASS=admin
  RABBITMQ_DEFAULT_HOST=queue

Build the containers::

  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml build

Bring up the containers in this order::

  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml up -d db queue
  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml up -d worker beat app

Some useful commands::

  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml logs -f
  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml images
  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml ps -q | xargs docker stats
  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml run app /venv/bin/python manage.py shell
  docker-compose -f docker-compose.yml -f docker-compose.deploy.yml run app /venv/bin/python manage.py shell --command="from eatsmart.locations.wake import tasks; tasks.import_wake_data.delay()"
