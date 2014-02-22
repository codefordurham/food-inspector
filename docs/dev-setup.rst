Eat Smart Development Setup
===========================

Front-end Setup
---------------

**Insert front-end development setup instructions here.**


Back-end API Setup
------------------

Below you will find basic setup and deployment instructions for the
Django-powered API back-end. **Back-end setup is not required if you only want to
develop front-end JavaScript/HTML/CSS.** To begin you should have the following
applications installed on your local development system:

- Python == 3.3
- `pip >= 1.4 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.10 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- Postgres >= 9.1
- PostGIS == 2.0
- git >= 1.7

The deployment uses SSH with agent forwarding so you'll need to enable agent
forwarding if it is not already by adding ``ForwardAgent yes`` to your SSH config.


Getting Started
~~~~~~~~~~~~~~~

If you need Python 3.3 installed, you can use this PPA::

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python3.3 python3.3-dev

The tool that we use to deploy code is called `Fabric
<http://docs.fabfile.org/>`_, which is not yet Python3 compatible. So,
we need to install that globally in our Python2 environment::

    sudo pip install fabric==1.8.1

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv --python=python3.3 eatsmart
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements/dev.txt

Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to use it::

    cp eatsmart/settings/local.example.py eatsmart/settings/local.py
    echo "export DJANGO_SETTINGS_MODULE=eatsmart.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

Exit the virtualenv and reactivate it to activate the settings just changed::

    deactivate
    workon eatsmart

Create the Postgres database and run the initial syncdb/migrate::

    createdb -E UTF-8 eatsmart
    psql eatsmart -c "CREATE EXTENSION postgis;"
    python manage.py syncdb
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver


Loading Durham Data
-------------------

Now you can import some data. To import Durham's data, you'll need to clone the
`Durham-Data repository <https://github.com/codefordurham/Durham-Data>`_ along
side your Durham-Restaurants repository, e.g.:

* /<my-projects-dir>/Durham-Restaurants/
* /<my-projects-dir>/Durham-Data/

Within your virtual environment, run the following command::

    python manage.py import_data

You should start to see output like this::

    Establishment ID: 58442 (46.45 records/sec)
    Establishment ID: 58942 (43.33 records/sec)
    Establishment ID: 60690 (44.71 records/sec)
    Establishment ID: 76487 (50.30 records/sec)
    Establishment ID: 85926 (48.40 records/sec)
    Establishment ID: 105925 (40.33 records/sec)
    ....
    Inspection ID: 2307977 (24.67 records/sec)
    Inspection ID: 894236 (39.92 records/sec)
    Inspection ID: 897425 (38.02 records/sec)
    Inspection ID: 902462 (39.50 records/sec)
    Inspection ID: 916736 (36.35 records/sec)

It may take a while to import on your machine.


Deployment
~~~~~~~~~~

You can deploy changes to a particular environment with
the ``deploy`` command. This takes an optional branch name to deploy. If the branch
is not given, it will use the default branch defined for this environment in
``env.branch``::

    fab production deploy

New requirements or South migrations are detected by parsing the VCS changes and
will be installed/run automatically.
