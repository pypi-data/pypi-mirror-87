# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Module to ease the creation and management of services.

The specific version for the services can be set through environment variables

.. code-block:: console

    $ export ES_VERSION=7.2.0

It can also use the centrally managed (supported) major version:

.. code-block:: console

    $ export ES_VERSION=ES_7_LATEST

Then it simply needs to boot up the services. Note that if no version was
exported in the environment, the CLI will use the default values set in
``env.py``.

.. code-block:: console

    $ docker-services-cli up es postgresql redis

And turn them of once they are not needed anymore:

.. code-block:: console

    $ docker-services-cli down
"""

from .version import __version__

__all__ = ("__version__",)
