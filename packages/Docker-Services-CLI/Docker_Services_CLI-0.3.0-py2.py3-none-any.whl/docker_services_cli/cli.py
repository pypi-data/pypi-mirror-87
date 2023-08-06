# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Docker-Services-CLI is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""CLI module."""

from distutils.sysconfig import get_python_lib
from functools import update_wrapper

import click

from .config import SERVICE_TYPES
from .env import normalize_service_name, override_default_env, \
    print_setup_env_config, set_env
from .services import services_down, services_up


def env_output(env_set_command):
    """Decorate command to print exportable environment settings."""
    if env_set_command not in ["export", "unset"]:
        click.secho("Wrong environment set command.", fg="red")
        exit(1)

    def print_env_output(func):
        @click.option(
            "--env",
            is_flag=True,
            default=False,
            help="Print export statements to set environment.",
        )
        def _print_env_output(*args, **kwargs):
            env = kwargs.pop("env", False)
            services = kwargs.get("services") or SERVICE_TYPES
            if env:
                # comment command output until env export
                click.echo(": '")
            click.get_current_context().invoke(func, *args, **kwargs)
            if env:
                # end of multiline comment, start of export statements
                click.echo("'")
                print_setup_env_config(
                    services,
                    click.get_current_context().info_name,
                    env_set_command=env_set_command,
                )

        return update_wrapper(_print_env_output, func)

    return print_env_output


def services_by_type(func):
    """Decorate command adding all service types as options.

    :param func: The function that implements the Click command to which the
        service types options will be added.

    :return: A wrapped function around the passed Click command which exposes
        all ``config.SERVICES_TYPES`` as Click options. The list of services
        by type is injected as ``services`` keyword argument.
    """

    def collect_services_by_type(*args, **kwargs):
        services = {}
        for service_type in SERVICE_TYPES:
            service = kwargs.pop(service_type)
            if service:
                services.setdefault(service_type, []).extend(
                    service if isinstance(service, list) else [service]
                )

        kwargs["services"] = services
        click.get_current_context().invoke(func, *args, **kwargs)

    def validate_service_name(ctx, service_type, services_list):
        available_services = SERVICE_TYPES.get(service_type.name, [])
        for service in services_list:
            if not (
                normalize_service_name(service)
                or normalize_service_name(service) in available_services
            ):
                raise click.BadParameter(
                    "{service} is not a valid service of type {type}. "
                    "Try one of: \n{available_services}".format(
                        service=service, type=service_type.name,
                        available_services=available_services
                    )
                )
        return list(services_list)

    for service_type in SERVICE_TYPES:
        click.option(
            "--{}".format(service_type),
            callback=validate_service_name,
            multiple=True,
            help="Specify which service should run as {0}. "
                 "Available {0} services: {1}.".format(
                     service_type,
                     ", ".join(SERVICE_TYPES.get(service_type))
                 )
        )(func)

    return update_wrapper(collect_services_by_type, func)


class ServicesCtx(object):
    """Context class for docker services cli."""

    def __init__(self, filepath, verbose):
        """Constructor."""
        self.filepath = filepath
        self.verbose = verbose


@click.group()
@click.version_option()
@click.option(
    "--filepath",
    "-f",
    required=False,
    default=f"{get_python_lib()}/docker_services_cli/docker-services.yml",
    type=click.Path(exists=True),
    help="Path to a docker compose file with the desired services definition.",
)
@click.option(
    "--verbose", is_flag=True, default=False, help="Verbose output.",
)
@click.pass_context
def cli(ctx, filepath, verbose):
    """Initialize CLI context."""
    set_env()
    ctx.obj = ServicesCtx(filepath=filepath, verbose=verbose)


@cli.command()
@click.option(
    "--no-wait",
    is_flag=True,
    help="Wait for services to be up (use healthchecks).",
)
@click.option(
    "--retries",
    default=6,
    type=int,
    help="Number of times to retry a service's healthcheck.",
)
@services_by_type
@env_output(env_set_command="export")
@click.pass_obj
def up(services_ctx, services, no_wait, retries):
    r"""Boots up the required services.

    Example: \n
    \t $ docker-services-cli up --db postgresql11

    Note: All services will be boot up if no service is specified.
    """
    _services = [s for services_list in services.values()
                 for s in services_list]

    # NOTE: docker-compose boots up all if none is provided
    if len(_services) == 1 and _services[0].lower() == "all":
        _services = []

    override_default_env(services_to_override=_services)
    click.secho("Environment setup", fg="green")

    normalized_services = [normalize_service_name(s) for s in _services]
    services_up(
        services=normalized_services,
        filepath=services_ctx.filepath,
        wait=(not no_wait),
        retries=retries,
        verbose=services_ctx.verbose,
    )
    click.secho("Services up!", fg="green")


@cli.command()
@env_output(env_set_command="unset")
@click.pass_obj
def down(services_ctx):
    """Boots down the required services."""
    services_down(filepath=services_ctx.filepath)
    click.secho("Services down!", fg="green")
