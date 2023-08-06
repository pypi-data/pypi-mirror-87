#! /usr/bin/env python3
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from typing import List

import click
import pandas as pd

from mafe.process import DistanceCalculator, normalize as proc_normalize, Cluster
from mafe.process.pca import Reducer
from mafe.scan import Scanner, TrackData, DEFAULT_STORE_EVERY


@click.group()
@click.option(
    '--tracks-csv', '-t', required=True, help='CSV file containing tracks'
)
@click.option(
    '--output', '-o', help='CSV file containing processed track data'
)
@click.pass_context
def cli(ctx, tracks_csv: str, output: str):
    ctx.ensure_object(dict)
    ctx.obj['tracks_csv'] = tracks_csv
    ctx.obj['output'] = output


@cli.command()
@click.pass_context
@click.option(
    '--base-folders', '-f', multiple=True, required=True, help='Directory to scan'
)
@click.option(
    '--max-track-length', '-m', type=int,
    help='Maximum track length, in seconds (longer tracks are ignored)'
)
@click.option(
    '--quiet', '-q', is_flag=True, default=False, help='Suppress warnings and progress messages'
)
@click.option(
    '--store-every', '-s', type=int, default=DEFAULT_STORE_EVERY, help='Store every n tracks'
)
def scan(
        ctx: click.Context, base_folders: List[str], max_track_length: int,
        quiet: bool, store_every: int
) -> None:
    if max_track_length is not None:
        TrackData.set_max_track_duration(max_track_length)

    scanner = Scanner(ctx.obj['tracks_csv'], base_folders, quiet, store_every)
    scanner.run()


@cli.command()
@click.pass_context
@click.option(
    '--method', '-m', type=click.Choice(['mean', 'min_max', 'zero_max'], case_sensitive=False),
    default='mean', help='Normalization method'
)
def normalize(ctx: click.Context, method: str) -> None:
    data = pd.read_csv(ctx.obj['tracks_csv'])
    normalized = proc_normalize(data, method=method)
    normalized.to_csv(ctx.obj['output'])


@cli.command()
@click.pass_context
def pca(ctx: click.Context) -> None:
    reducer = Reducer(ctx.obj['tracks_csv'])
    reducer.run().to_csv(ctx.obj['output'])


@cli.command()
@click.pass_context
@click.option(
    '--verbose', '-v', is_flag=True, default=False, help='Show progress info'
)
def distance(ctx: click.Context, verbose: bool) -> None:
    calculator = DistanceCalculator(ctx.obj['tracks_csv'], ctx.obj['output'])
    calculator.run(verbose=verbose)


@cli.command()
@click.option(
    '--num-clusters', '-n', required=True, type=int, help='Number of clusters to compute'
)
@click.option(
    '--max-iter', '-m', type=int, default=300, help='Maximum iterations to run'
)
@click.option(
    '--visualize', '-V', is_flag=True, default=False, help='Visualize clusters'
)
@click.option(
    '--num-samples', '-N', type=int, default=None, help='Number of points for cluster visualization'
)
@click.option(
    '--image-file', '-I', default=None, help='Cluster visualization image file'
)
@click.pass_context
def cluster(  # pylint: disable=too-many-arguments
        ctx: click.Context,
        num_clusters: int, max_iter: int, visualize: bool, num_samples: int, image_file: str
) -> None:
    clusterer = Cluster(ctx.obj['tracks_csv'], num_clusters)
    clusterer.run(max_iter).to_csv(ctx.obj['output'])
    if visualize:
        clusterer.visualize(n_samples=num_samples, image_file=image_file)
