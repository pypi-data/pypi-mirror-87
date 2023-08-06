# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inventory',
 'inventory.admin',
 'inventory.management',
 'inventory.management.commands',
 'inventory.migrations',
 'inventory.models',
 'inventory.tests',
 'inventory.tests.fixtures',
 'inventory_project',
 'inventory_project.settings',
 'inventory_project.tests']

package_data = \
{'': ['*'],
 'inventory': ['locale/de/LC_MESSAGES/*',
               'locale/en/LC_MESSAGES/*',
               'static/*',
               'templates/admin/inventory/item/*'],
 'inventory_project': ['templates/admin/*']}

install_requires = \
['bx_py_utils==0.0.4',
 'colorama',
 'colorlog',
 'django-admin-sortable2',
 'django-axes',
 'django-ckeditor',
 'django-dbbackup',
 'django-debug-toolbar',
 'django-import-export',
 'django-processinfo',
 'django-reversion-compare',
 'django-tagulous',
 'django-tools>=0.48.2',
 'django>=2.2.0,<2.3.0',
 'gunicorn',
 'pillow',
 'requests']

extras_require = \
{'docker': ['docker-compose'], 'postgres': ['psycopg2-binary']}

entry_points = \
{'console_scripts': ['manage = inventory_project.manage:main',
                     'publish = inventory_project.publish:publish',
                     'update_rst_readme = '
                     'inventory_project.publish:update_readme']}

setup_kwargs = {
    'name': 'pyinventory',
    'version': '0.8.0rc1',
    'description': 'Web based management to catalog things including state and location etc. using Python/Django.',
    'long_description': '===========\nPyInventory\n===========\n\nWeb based management to catalog things including state and location etc. using Python/Django.\n\nThe project is in an early stage of development. Some things are already implemented and usable. But there is still a lot to do.\n\nPull requests welcome!\n\n+-----------------------------------+-------------------------------------------------+\n| |Build Status on github|          | `github.com/jedie/PyInventory/actions`_         |\n+-----------------------------------+-------------------------------------------------+\n| |Build Status on travis-ci.org|   | `travis-ci.org/jedie/PyInventory`_              |\n+-----------------------------------+-------------------------------------------------+\n| |Coverage Status on codecov.io|   | `codecov.io/gh/jedie/PyInventory`_              |\n+-----------------------------------+-------------------------------------------------+\n| |Coverage Status on coveralls.io| | `coveralls.io/r/jedie/PyInventory`_             |\n+-----------------------------------+-------------------------------------------------+\n| |Status on landscape.io|          | `landscape.io/github/jedie/PyInventory/master`_ |\n+-----------------------------------+-------------------------------------------------+\n\n.. |Build Status on github| image:: https://github.com/jedie/PyInventory/workflows/test/badge.svg?branch=master\n.. _github.com/jedie/PyInventory/actions: https://github.com/jedie/PyInventory/actions\n.. |Build Status on travis-ci.org| image:: https://travis-ci.org/jedie/PyInventory.svg\n.. _travis-ci.org/jedie/PyInventory: https://travis-ci.org/jedie/PyInventory/\n.. |Coverage Status on codecov.io| image:: https://codecov.io/gh/jedie/PyInventory/branch/master/graph/badge.svg\n.. _codecov.io/gh/jedie/PyInventory: https://codecov.io/gh/jedie/PyInventory\n.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/jedie/PyInventory/badge.svg\n.. _coveralls.io/r/jedie/PyInventory: https://coveralls.io/r/jedie/PyInventory\n.. |Status on landscape.io| image:: https://landscape.io/github/jedie/PyInventory/master/landscape.svg\n.. _landscape.io/github/jedie/PyInventory/master: https://landscape.io/github/jedie/PyInventory/master\n\n-----\nabout\n-----\n\nThe focus of this project is on the management of retro computing hardware.\n\nPlan:\n\n* Web-based\n\n* Multiuser ready\n\n* Chaotic warehousing\n\n    * Grouped "Storage": Graphics card is in computer XY\n\n* Data structure kept as general as possible\n\n* You should be able to add the following to the items:\n\n    * Storage location\n\n    * State\n\n    * Pictures\n\n    * URLs\n\n    * receiving and delivering (when, from whom, at what price, etc.)\n\n    * Information: Publicly visible yes/no\n\n* A public list of existing items (think about it, you can set in your profile if you want to)\n\n* administration a wish & exchange list\n\nany many more... ;)\n\n-----------------\nProject structure\n-----------------\n\nThere are two main directories:\n\n+---------------------+--------------------------------------------+\n| directory           | description                                |\n+=====================+============================================+\n| **`/src/`_**        | The main PyInventory source code           |\n+---------------------+--------------------------------------------+\n| **`/deployment/`_** | deploy PyInventory for production use case |\n+---------------------+--------------------------------------------+\n\n.. _/src/: https://github.com/jedie/PyInventory/tree/master/src\n.. _/deployment/: https://github.com/jedie/PyInventory/tree/master/deployment\n\n-------\ninstall\n-------\n\nThere exists two kind of installation/usage:\n\n* local development installation using poetry\n\n* production use with docker-compose\n\nThis README contains only the information about local development installation.\n\nRead `/deployment/README <https://github.com/jedie/PyInventory/tree/master/deployment#readme>`_ for instruction to install PyInventory on a root server.\n\nprepare\n=======\n\n::\n\n    ~$ git clone https://github.com/jedie/PyInventory.git\n    ~$ cd PyInventory/\n    ~/PyInventory$ make\n    _________________________________________________________________\n    PyInventory - *dev* Makefile\n    \n    install-poetry         install or update poetry\n    install                install PyInventory via poetry\n    manage-update          Collectstatic + makemigration + migrate\n    update                 update the sources and installation\n    lint                   Run code formatters and linter\n    fix-code-style         Fix code formatting\n    tox-listenvs           List all tox test environments\n    tox                    Run pytest via tox with all environments\n    tox-py36               Run pytest via tox with *python v3.6*\n    tox-py37               Run pytest via tox with *python v3.7*\n    tox-py38               Run pytest via tox with *python v3.8*\n    pytest                 Run pytest\n    update-rst-readme      update README.rst from README.creole\n    publish                Release new version to PyPi\n    run-dev-server         Run the django dev server in endless loop.\n    createsuperuser        Create super user\n    messages               Make and compile locales message files\n    dbbackup               Backup database\n    dbrestore              Restore a database backup\n    run-docker-dev-server  Start docker containers with current dev source code\n\nlocal development installation\n==============================\n\n::\n\n    # install or update Poetry:\n    ~/PyInventory$ make install-poetry\n    \n    # install PyInventory via poetry:\n    ~/PyInventory$ make install\n    ...\n    \n    # Collectstatic + makemigration + migrate:\n    ~/PyInventory$ make manage-update\n    \n    # Create a django super user:\n    ~/PyInventory$ ./manage.sh createsuperuser\n    \n    # start local dev. web server:\n    ~/PyInventory$ make run-dev-server\n\nThe web page is available via: ``http://127.0.0.1:8000/``\n\nlocal docker dev run\n====================\n\nYou can run the deployment docker containers with current source code with:\n\n::\n\n    ~/PyInventory$ make run-docker-dev-server\n\nJust hit Cntl-C to stop the containers\n\n-----------\nScreenshots\n-----------\n\n|PyInventory v0.2.0 screenshot 1.png|\n\n.. |PyInventory v0.2.0 screenshot 1.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.2.0 screenshot 1.png\n\n----\n\n|PyInventory v0.1.0 screenshot 2.png|\n\n.. |PyInventory v0.1.0 screenshot 2.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 2.png\n\n----\n\n|PyInventory v0.1.0 screenshot 3.png|\n\n.. |PyInventory v0.1.0 screenshot 3.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 3.png\n\n----\n\n------------------\nMulti user support\n------------------\n\nPyInventory supports multiple users. The idea:\n\n* Every normal user sees only his own created database entries\n\n* All users used the Django admin\n\nNote: All created Tags are shared for all existing users!\n\nSo setup a normal user:\n\n* Set "Staff status"\n\n* Unset "Superuser status"\n\n* Add user to "normal_user" group\n\n* Don\'t add any additional permissions\n\ne.g.:\n\n|normal user example|\n\n.. |normal user example| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory normal user example.png\n\n------------------------------\nBackwards-incompatible changes\n------------------------------\n\nv0.7.0\n======\n\nDocker-Compose usage: The MEDIA files was not stored on a docker volumes.\n\nYou should backup rhe media files **before** update the containers!\n\ne.g.:\n\n::\n\n    ~/PyInventory/deployment$ make shell_inventory\n    root@inventory:/django# cp -Rfv /media/ /django_volumes/media/\n\nThe files are stored locally here:\n\n::\n\n    ~/PyInventory/deployment$ ls -la volumes/django/media/\n\nNow, update the containers and copy the files back.\n\nv0.5.0\n======\n\nGit branches "master" and "deployment" was merged into one.\nFiles are separated into: "/src/" and "/development/"\n\n-------\nhistory\n-------\n\n* `compare v0.7.0...master <https://github.com/jedie/PyInventory/compare/v0.7.0...master>`_ **dev** \n\n    * tbc\n\n* `v0.8.0rc1 - 06.12.2020 <https://github.com/jedie/PyInventory/compare/v0.7.0...v0.8.0rc1>`_ \n\n    * Outsource the "MEDIA file serve" part into `django.tools.serve_media_app <https://github.com/jedie/django-tools/tree/master/django_tools/serve_media_app#readme>`_\n\n* `v0.7.0 - 23.11.2020 <https://github.com/jedie/PyInventory/compare/v0.6.0...v0.7.0>`_ \n\n    * Change deployment setup:\n\n        * Replace uwsgi with gunicorn\n\n        * make deploy setup more generic by renaming "inventory" to "django"\n\n        * Bugfix MEDIA path: store the files on a docker volumes\n\n        * run app server as normal user and not root\n\n        * pull all docker images before build\n\n* `v0.6.0 - 15.11.2020 <https://github.com/jedie/PyInventory/compare/v0.5.0...v0.6.0>`_ \n\n    * User can store images to every item: The image can only be accessed by the same user.\n\n* `v0.5.0 - 14.11.2020 <https://github.com/jedie/PyInventory/compare/v0.4.2...v0.5.0>`_ \n\n    * Merge separate git branches into one: "/src/" and "/development/" `#19 <https://github.com/jedie/PyInventory/issues/19>`_\n\n* `v0.4.2 - 13.11.2020 <https://github.com/jedie/PyInventory/compare/v0.4.1...v0.4.2>`_ \n\n    * Serve static files by Caddy\n\n    * Setup CKEditor file uploads: Store files into random sub directory\n\n    * reduce CKEditor plugins\n\n* `v0.4.1 - 2.11.2020 <https://github.com/jedie/PyInventory/compare/v0.4.0...v0.4.1>`_ \n\n    * Small bugfixes\n\n* `v0.4.0 - 1.11.2020 <https://github.com/jedie/PyInventory/compare/v0.3.2...v0.4.0>`_ \n\n    * Move docker stuff and production use information into separate git branch\n\n    * Add django-axes: keeping track of suspicious logins and brute-force attack blocking\n\n    * Add django-processinfo: collect information about the running server processes\n\n* `v0.3.2 - 26.10.2020 <https://github.com/jedie/PyInventory/compare/v0.3.0...v0.3.2>`_ \n\n    * Bugfix missing translations\n\n* `v0.3.0 - 26.10.2020 <https://github.com/jedie/PyInventory/compare/v0.2.0...v0.3.0>`_ \n\n    * setup production usage:\n\n        * Use `caddy server <https://caddyserver.com/>`_ as reverse proxy\n\n        * Use uWSGI as application server\n\n        * autogenerate ``secret.txt`` file for ``settings.SECRET_KEY``\n\n        * Fix settings\n\n    * split settings for local development and production use\n\n    * Bugfix init: move "setup user group" from checks into "post migrate" signal handler\n\n    * Bugfix for using manage commands ``dumpdata`` and ``loaddata``\n\n* `v0.2.0 - 24.10.2020 <https://github.com/jedie/PyInventory/compare/v0.1.0...v0.2.0>`_ \n\n    * Simplify item change list by nested item\n\n    * Activate Django-Import/Export\n\n    * Implement multi user usage\n\n    * Add Django-dbbackup\n\n    * Add docker-compose usage\n\n* `v0.1.0 - 17.10.2020 <https://github.com/jedie/PyInventory/compare/v0.0.1...v0.1.0>`_ \n\n    * Enhance models, admin and finish project setup\n\n* v0.0.1 - 14.10.2020\n\n    * Just create a pre-alpha release to save the PyPi package name ;)\n\n-----\nlinks\n-----\n\n+----------+------------------------------------------+\n| Homepage | `http://github.com/jedie/PyInventory`_   |\n+----------+------------------------------------------+\n| PyPi     | `https://pypi.org/project/PyInventory/`_ |\n+----------+------------------------------------------+\n\n.. _http://github.com/jedie/PyInventory: http://github.com/jedie/PyInventory\n.. _https://pypi.org/project/PyInventory/: https://pypi.org/project/PyInventory/\n\nDiscuss here:\n\n* `vogons.org Forum Thread (en) <https://www.vogons.org/viewtopic.php?f=5&t=77285>`_\n\n* `Python-Forum (de) <https://www.python-forum.de/viewtopic.php?f=9&t=50024>`_\n\n* `VzEkC e. V. Forum Thread (de) <https://forum.classic-computing.de/forum/index.php?thread/21738-opensource-projekt-pyinventory-web-basierte-verwaltung-um-seine-dinge-zu-katalog/>`_\n\n* `dosreloaded.de Forum Thread (de) <https://dosreloaded.de/forum/index.php?thread/3702-pyinventory-retro-sammlung-katalogisieren/>`_\n\n--------\ndonation\n--------\n\n* `paypal.me/JensDiemer <https://www.paypal.me/JensDiemer>`_\n\n* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2Fjedie%2FPyInventory%2F>`_\n\n* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_\n\n------------\n\n``Note: this file is generated from README.creole 2020-12-06 19:20:04 with "python-creole"``',
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
