Server Provisioning
========================


Dokku Setup
-----------

Install dokku plugins::

    ssh copelco@prism sudo dokku plugin:install https://github.com/michaelshobbs/dokku-logspout.git
    ssh copelco@prism sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
    ssh copelco@prism sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
    ssh copelco@prism sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis
    ssh prism logspout:server syslog+tls://logs2.papertrailapp.com:20851


Example Project
---------------

Let's deploy the example Python project::

  git clone https://github.com/heroku/python-sample.git
  cd python-sample
  git remote add dokku prism:python-sample
  git push dokku master

Enable SSL::

  ssh prism config:set python-sample --no-restart DOKKU_LETSENCRYPT_EMAIL='copelco@caktusgroup.com'
  ssh prism letsencrypt python-sample
  ssh prism letsencrypt:cron-job --add python-sample


NC Food Inspector
-----------------

Create a storage directory and set its ownership as documented at http://dokku.viewdocs.io/dokku/advanced-usage/persistent-storage/, something like::

    ssh copelco@prism sudo mkdir /var/lib/dokku/data/storage/ncfoodinspector
    ssh copelco@prism sudo chown 32767:32767 /var/lib/dokku/data/storage/ncfoodinspector

Now you should be able to set up the rest::

    # Create an app
    $ ssh prism apps:create ncfoodinspector

    # Set deploy branch
    ssh prism config:set ncfoodinspector --no-restart DOKKU_DEPLOY_BRANCH=dokku
    # SECRET_KEY
    ssh prism config:set ncfoodinspector --no-restart SECRET_KEY=<fill-me-in>
    # ENVIRONMENT
    ssh prism config:set ncfoodinspector --no-restart ENVIRONMENT=production
    # POSTGRES_DATABASE_SCHEME for postgis
    ssh prism config:set ncfoodinspector --no-restart POSTGRES_DATABASE_SCHEME=postgis

    # Mount the directory from the dokku server inside our container at /storage
    $ ssh prism storage:mount ncfoodinspector /var/lib/dokku/data/storage/ncfoodinspector:/storage

    # To create a PostGIS-enabled database, connect to the dokku host and set the base image before running postgres:create:
    ssh copelco@prism
    export POSTGRES_IMAGE="mdillon/postgis"
    export POSTGRES_IMAGE_VERSION="9.6"
    dokku postgres:create ncfoodinspector

    # If successful, you can connect and create the PostgreSQL exention:
    $ ssh prism postgres:connect ncfoodinspector
    ncfoodinspector=# CREATE EXTENSION postgis;

    # If you have a backup whose data you want to use on this site, restore from it
    # (It should be in Postgres custom dump format.)
    # The postgres:import does not do the restore with ``--if-exists`` as it
    # probably should, so you will see a bunch of errors about things not
    # existing, which you can ignore. Unfortunately, this will make it hard to
    # spot whether there were other errors that you should pay attention to,
    # but try to look for any other kinds of errors in the output.
    $ ssh prism postgres:import ncfoodinspector < backupfile.dump

    # Now link the database to our app
    $ ssh prism postgres:link ncfoodinspector ncfoodinspector

    # Configure redis
    $ ssh prism redis:create ncfoodinspector
    $ ssh prism redis:link ncfoodinspector ncfoodinspector

    # Tell local git about the dokku server and push
    $ git remote add prism prism:ncfoodinspector
    $ git push prism dokku

    # Setup SSL
    ssh prism config:set ncfoodinspector --no-restart DOKKU_LETSENCRYPT_EMAIL='code-for-durham-team@codeforamerica.org'
    ssh prism letsencrypt ncfoodinspector
    ssh prism letsencrypt:cron-job --add ncfoodinspector

    # Manually kick off import
    ssh prism run ncfoodinspector python manage.py shell
    >>> from eatsmart.locations.wake.tasks import import_wake_data
    >>> import_wake_data.delay()
