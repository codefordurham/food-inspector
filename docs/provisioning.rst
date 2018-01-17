Server Provisioning
========================


NC Food Inspector
-----------------

Create a storage directory and set its ownership as documented at http://dokku.viewdocs.io/dokku/advanced-usage/persistent-storage/, something like::

    ssh copelco@cfd sudo mkdir /var/lib/dokku/data/storage/ncfoodinspector
    ssh copelco@cfd sudo chown 32767:32767 /var/lib/dokku/data/storage/ncfoodinspector

Now you should be able to set up the rest::

    # Create an app
    $ ssh cfd apps:create ncfoodinspector

    # Set deploy branch
    ssh cfd config:set ncfoodinspector --no-restart DOKKU_DEPLOY_BRANCH=master
    # SECRET_KEY
    ssh cfd config:set ncfoodinspector --no-restart SECRET_KEY=<fill-me-in>
    # ENVIRONMENT
    ssh cfd config:set ncfoodinspector --no-restart ENVIRONMENT=production
    # POSTGRES_DATABASE_SCHEME for postgis
    ssh cfd config:set ncfoodinspector --no-restart POSTGRES_DATABASE_SCHEME=postgis

    # Mount the directory from the dokku server inside our container at /storage
    $ ssh cfd storage:mount ncfoodinspector /var/lib/dokku/data/storage/ncfoodinspector:/storage

    # To create a PostGIS-enabled database, connect to the dokku host and set the base image before running postgres:create:
    ssh copelco@cfd
    export POSTGRES_IMAGE="mdillon/postgis"
    export POSTGRES_IMAGE_VERSION="9.6"
    dokku postgres:create ncfoodinspector

    # If successful, you can connect and create the PostgreSQL extension:
    $ ssh cfd postgres:connect ncfoodinspector
    ncfoodinspector=# CREATE EXTENSION postgis;

    # If you have a backup whose data you want to use on this site, restore from it
    # (It should be in Postgres custom dump format.)
    # The postgres:import does not do the restore with ``--if-exists`` as it
    # probably should, so you will see a bunch of errors about things not
    # existing, which you can ignore. Unfortunately, this will make it hard to
    # spot whether there were other errors that you should pay attention to,
    # but try to look for any other kinds of errors in the output.
    $ ssh cfd postgres:import ncfoodinspector < backupfile.dump

    # Now link the database to our app
    $ ssh cfd postgres:link ncfoodinspector ncfoodinspector

    # Configure redis
    $ ssh cfd redis:create ncfoodinspector
    $ ssh cfd redis:link ncfoodinspector ncfoodinspector

    # Tell local git about the dokku server and push
    $ git remote add cfd cfd:ncfoodinspector
    $ git push cfd dokku

    # Domains
    ssh cfd domains:add ncfoodinspector ncfoodinspector.com
    ssh cfd redirect:set ncfoodinspector www.ncfoodinspector.com ncfoodinspector.com

    # Setup SSL
    ssh cfd config:set ncfoodinspector --no-restart DOKKU_LETSENCRYPT_EMAIL='code-for-durham-team@codeforamerica.org'
    ssh cfd letsencrypt ncfoodinspector
    ssh cfd letsencrypt:cron-job --add ncfoodinspector

    # Manually kick off import
    ssh cfd run ncfoodinspector python manage.py shell
    >>> from eatsmart.locations.wake.tasks import import_wake_data
    >>> import_wake_data.delay()
