Local Docker Development Instructions
=====================================


Mac-specific
------------

First install `homebrew <https://brew.sh/>`_ and `Virtualbox <https://www.virtualbox.org/>`_.

Update ``homebrew`` and install ``docker`` utilities::

  brew update
  brew upgrade
  brew install docker docker-machine docker-compose

Create a virtual machine to run docker::

  docker-machine create dockervm --driver virtualbox --virtualbox-disk-size "10000" --virtualbox-cpu-count 2 --virtualbox-memory "4096"

Setup the environment for the docker client::

  # make sure development VM is running in VirtualBox
  docker-machine ls
  # restart the machine if it is not running
  docker-machine restart dockervm
  # load the machine environment
  eval $(docker-machine env dockervm)


Initial Local Development Setup
-------------------------------

Configure environment to use docker settings file::

  echo "DJANGO_SETTINGS_MODULE=eatsmart.settings.docker" > .env

Build the containers::

  docker-compose build

Bring up the containers in this order (any way around this to avoid errors?)::

  docker-compose up -d db
  docker-compose up -d app

To view in a browser, obtain the IP address of the dockervm::

  docker-machine ip dockervm

Now visit http://<ip>:8000 in your browser.


Load DB Dump
~~~~~~~~~~~~

The easiest way to get data is to load a db dump::

  wget https://s3.amazonaws.com/ncfoodinspector/eatsmart.tar.zip
  unzip eatsmart.tar.zip
  docker exec -i "`docker-compose ps -q db`" pg_restore --data-only --clean --no-acl --no-owner -U "postgres" -d "postgres" < eatsmart.tar

You'll see a few errors for ``auth_permission``, ``django_content_type``, and ``django_migrations`` tables, but it will still work.

  .. docker-compose run app /venv/bin/python manage.py migrate
