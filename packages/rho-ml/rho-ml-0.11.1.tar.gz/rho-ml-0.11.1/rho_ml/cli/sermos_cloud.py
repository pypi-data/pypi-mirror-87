""" Command Line Utilities for Sermos Cloud Rho Model APIs
"""
import json
import logging
import click
from rho_ml import search_rho_model

logger = logging.getLogger(__name__)


@click.group()
def sermos_cloud():
    """ Sermos Cloud command group.
    """


@sermos_cloud.command()
@click.option('--model-name', required=False, default=None)
@click.option('--version-pattern', required=False, default=None)
@click.option('--access-key', required=False, default=None)
@click.option('--search-model-endpoint', required=False, default=None)
def search(access_key: str = None,
           model_name: str = None,
           version_pattern: str = None,
           search_model_endpoint: str = None):
    """ Search for available models against Sermos Admin's public API.

        Arguments::

            access-key (optional): Defaults to checking the environment for
                `SERMOS_ACCESS_KEY`. If not found, will exit.

            model-name (optional): Model name to search for. Accepts wildcard.
                e.g. MyModelName, MyModel* If none provided, will search
                against all model names.

            version-pattern (optional): Version to search for. Accepts wildcard.
                e.g. 1.1.1, 1.*.* If none provided, will search against all
                versions.

            search-url (optional): Defaults to primary Sermos search-models
                endpoint. Only modify this if there is a specific, known reason
                to do so.
    """
    resp = search_rho_model(model_name, version_pattern, access_key,
                            search_model_endpoint)
    click.echo(f'{json.dumps(resp, indent=2)}')
