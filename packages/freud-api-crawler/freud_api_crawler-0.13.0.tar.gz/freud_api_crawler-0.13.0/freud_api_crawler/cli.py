"""Console script for freud_api_crawler."""
import os
import sys
import click

from . import freud_api_crawler as frd
from . file_utils import flatten_files as flatten


@click.command()
@click.argument('user', envvar='FRD_USER')
@click.argument('pw', envvar='FRD_PW')
@click.option('-m', default='a10e8c78-adad-4ca2-bfcb-b51bedcd7b58', show_default=True)
def cli(user, pw, m):
    """Console script for freud_api_crawler."""

    auth_items = frd.get_auth_items(user, pw)
    frd_manifestation = frd.FrdManifestation(
        auth_items=auth_items,
        manifestation_id=m
    )
    xml = frd_manifestation.make_xml(save=True)
    click.echo(
        click.style(
            f"processed Manifestation\n###\n {frd_manifestation.md__title}\
            {frd_manifestation.manifestation_id}\n###", fg='green'
        )
    )


@click.command()  # pragma: no cover
@click.argument('user', envvar='FRD_USER')  # pragma: no cover
@click.argument('pw', envvar='FRD_PW')  # pragma: no cover
@click.option('-w', default='9d035a03-28d7-4013-adaf-63337d78ece4', show_default=True)  # pragma: no cover
@click.option('-s', default='/home/csae8092/freud_data_cli', show_default=True)  # pragma: no cover
def download_work(user, pw, w, s):  # pragma: no cover
    """Console script to download all manifestations of a singel work."""
    auth_items = frd.get_auth_items(user, pw)
    werk_obj = frd.FrdWerk(
        auth_items=auth_items, werk_id=w
    )
    rel_manifestations = werk_obj.manifestations
    for x in rel_manifestations:
        frd_man = frd.FrdManifestation(
            out_dir=s,
            manifestation_id=x['man_id'],
            auth_items=auth_items
        )
        frd_man.make_xml(save=True, limit=False)
    click.echo(
        click.style(
            f"finished download\n{werk_obj.manifestations_count} Manifestations for {werk_obj.md__title} into {s}",
            fg='green'
        )
    )


@click.command()  # pragma: no cover
@click.option('-s', default='/home/csae8092/freud_data_cli/werke/drei-abhandlungen-zur-sexualtheorie', show_default=True)  # pragma: no cover
def flatten_files(s):  # pragma: no cover
    """Console script to flatten XML/TEI files of a work."""
    flattend = flatten(s)
    click.echo(
        click.style(
            f"finished",
            fg='green'
        )
    )
