# Copyright 2019 Cognite AS
# flake8: noqa
# mypy: allow-untyped-defs


def get_version():
    try:
        import pkg_resources

        return pkg_resources.get_distribution("cognite-seismic-sdk").version
    except ImportError:
        return "0.0.0-dev"
