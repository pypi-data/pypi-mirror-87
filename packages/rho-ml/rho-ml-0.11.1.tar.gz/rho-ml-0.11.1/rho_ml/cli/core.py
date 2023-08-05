""" Primary CLI group entrypoint
"""
import click
from rho_ml.cli.sermos_cloud import sermos_cloud

rho_ml = click.CommandCollection(sources=[
    sermos_cloud,
])
