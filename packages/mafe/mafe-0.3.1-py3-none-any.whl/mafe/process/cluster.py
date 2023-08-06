__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from typing import Tuple

import pandas as pd
from sklearn.cluster import KMeans

from mafe.process.scatter_plot import ScatterPlot
from mafe.scan import TrackData


def k_means(tracks: pd.DataFrame, n_clusters: int, max_iter: int) -> KMeans:
    return KMeans(n_clusters=n_clusters, max_iter=max_iter).fit(tracks)


class Cluster:

    def __init__(
            self, tracks_csv: str, n_clusters: int, text_cols: Tuple[str, ...] = None
    ) -> None:
        self.tracks = pd.read_csv(tracks_csv)
        self.text_cols = list(TrackData.STRING_COLUMNS) if text_cols is None else text_cols
        self.n_clusters = n_clusters

    def run(self, n_iter: int = 300) -> pd.DataFrame:
        numbers_only = self.tracks.drop(self.text_cols, axis='columns').dropna(axis='columns')
        kmeans = k_means(numbers_only, self.n_clusters, n_iter)
        self.tracks.insert(1, 'cluster', kmeans.labels_, True)
        return self.tracks

    def visualize(self, n_samples: int = None, image_file: str = None) -> None:
        visualizer = ScatterPlot('cluster', ['0', '1', '2'], image_file)
        data = self._reduce_data(n_samples)

        for _, row in data.iterrows():
            visualizer.plot_data_point(row)

        visualizer.show_or_save()

    def _reduce_data(self, n_samples: int) -> pd.DataFrame:
        if 'cluster' not in self.tracks.columns:
            raise ValueError('Run clustering before visualizing')
        try:
            data = self.tracks[['cluster', '0', '1', '2']]
        except KeyError as error:
            raise ValueError('Run dimensionality reduction before visualizing') from error

        if n_samples is not None and n_samples < len(data):
            data = data.sample(n=n_samples)
        return data
