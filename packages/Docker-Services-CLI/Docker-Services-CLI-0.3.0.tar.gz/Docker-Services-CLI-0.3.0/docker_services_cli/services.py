# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Services module."""

import time
from os import path
from subprocess import PIPE, Popen, check_call

import click

from .config import DOCKER_SERVICES_FILEPATH, MYSQL, POSTGRESQL, SERVICE_TYPES


def _run_healthcheck_command(command, verbose=False):
    """Runs a given command, returns True if it succeeds, False otherwise."""
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    output = output.decode("utf-8")
    error = error.decode("utf-8")
    if p.returncode == 0:
        if verbose:
            click.secho(output, fg="green")
        return True
    if p.returncode != 0:
        if verbose:
            click.secho(
                f"Healthcheck failed.\nOutput: {output}\nError:{error}",
                fg="red"
            )
        return False


def es_healthcheck(*args, **kwargs):
    """Elasticsearch healthcheck."""
    verbose = kwargs['verbose']

    return _run_healthcheck_command([
        "curl",
        "-f",
        "localhost:9200/_cluster/health?wait_for_status=green"
    ], verbose)


def postgresql_healthcheck(*args, **kwargs):
    """Postgresql healthcheck."""
    filepath = kwargs['filepath']
    verbose = kwargs['verbose']

    return _run_healthcheck_command([
        "docker-compose",
        "--file",
        filepath,
        "exec",
        "-T",
        "postgresql",
        "bash",
        "-c",
        "pg_isready",
    ], verbose)


def mysql_healthcheck(*args, **kwargs):
    """Mysql healthcheck."""
    filepath = kwargs['filepath']
    verbose = kwargs['verbose']
    password = \
        MYSQL["CONTAINER_CONFIG_ENVIRONMENT_VARIABLES"]["MYSQL_ROOT_PASSWORD"]

    return _run_healthcheck_command([
        "docker-compose",
        "--file",
        filepath,
        "exec",
        "-T",
        "mysql",
        "bash",
        "-c",
        f"mysql -p{password} -e \"select Version();\"",
    ], verbose)


def rabbitmq_healthcheck(*args, **kwargs):
    """Rabbitmq healthcheck."""
    filepath = kwargs['filepath']
    verbose = kwargs['verbose']

    return _run_healthcheck_command([
        "docker-compose",
        "--file",
        filepath,
        "exec",
        "-T",
        "rabbitmq",
        "bash",
        "-c",
        "rabbitmq-diagnostics check_running"
    ], verbose)


def redis_healthcheck(*args, **kwargs):
    """Redis healthcheck."""
    filepath = kwargs['filepath']
    verbose = kwargs['verbose']

    return _run_healthcheck_command([
        "docker-compose",
        "--file",
        filepath,
        "exec",
        "-T",
        "redis",
        "bash",
        "-c",
        "redis-cli ping",
        "|",
        "grep 'PONG'",
        "&>/dev/null;",
    ], verbose)


HEALTHCHECKS = {
    "elasticsearch": es_healthcheck,
    "postgresql": postgresql_healthcheck,
    "mysql": mysql_healthcheck,
    "rabbitmq": rabbitmq_healthcheck,
    "redis": redis_healthcheck,
}
"""Health check functions module path, as string."""


def wait_for_services(services, filepath=DOCKER_SERVICES_FILEPATH,
                      max_retries=6, verbose=False):
    """Wait for services to be up.

    It performs configured healthchecks in a serial fashion, following the
    order given in the ``up`` command. If the services is an empty list, to be
    compliant with `docker-compose` it will perform the healthchecks of all the
    services.
    """
    if len(services) == 0:
        services = HEALTHCHECKS.keys()

    for service in services:
        exp_backoff_time = 2
        try_ = 1
        # Using plain __import__ to avoid depending on invenio-base
        check = HEALTHCHECKS[service]
        ready = check(filepath=filepath, verbose=verbose)
        while not ready and try_ < max_retries:
            click.secho(
                f"{service} not ready at {try_} retries, waiting "
                f"{exp_backoff_time}s",
                fg="yellow"
            )
            try_ += 1
            time.sleep(exp_backoff_time)
            exp_backoff_time *= 2
            ready = check(filepath=filepath, verbose=verbose)

        if not ready:
            click.secho(f"Unable to boot up {service}", fg="red")
            exit(1)
        else:
            click.secho(f"{service} up and running!", fg="green")


def services_up(services, filepath=DOCKER_SERVICES_FILEPATH, wait=True,
                retries=6, verbose=False):
    """Start the given services up.

    docker-compose is smart about not rebuilding an image if
    there is no need to, so --build is not a slow default. In addition
    ``--detach`` is not supported in 1.17.0 or previous.
    """
    services = services or [service
                            for _, services in SERVICE_TYPES.items()
                            for service in services]
    if not path.exists(filepath):
        click.secho(f"Filepaht {filepath} for docker-services.yml file does"
                    "not exist.", fg="red")
        exit(1)

    command = ["docker-compose", "--file", filepath, "up", "-d"]
    command.extend(services)

    check_call(command)
    if wait:
        wait_for_services(services, filepath, max_retries=retries,
                          verbose=verbose)


def services_down(filepath=DOCKER_SERVICES_FILEPATH):
    """Stops the given services.

    It does not requries the services. It stops containers and removes
    containers, networks, volumes, and images created by ``up``.
    """
    command = ["docker-compose", "--file", filepath, "down"]

    check_call(command)
