__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

from mafe.scan import TrackData


def pca(data: pd.DataFrame, total_variance_ratio: float = 0.99) -> Tuple[PCA, np.ndarray]:
    reducer = PCA(total_variance_ratio, svd_solver='full')
    transformed = reducer.fit_transform(data.to_numpy())
    return reducer, transformed


class Reducer:
    def __init__(
            self, tracks_csv: str, total_variance_ratio: float = 0.99,
            num_cols: Tuple[str, ...] = None, text_cols: Tuple[str, ...] = None
    ) -> None:
        self.tracks = pd.read_csv(tracks_csv)
        self.total_variance_ratio = total_variance_ratio
        self.num_cols = TrackData.numerical_columns() if num_cols is None else num_cols
        self.text_cols = TrackData.STRING_COLUMNS if text_cols is None else text_cols
        self.reducer: PCA = None

    def run(self) -> pd.DataFrame:
        numbers_only = self.tracks[list(self.num_cols)].dropna(axis='columns')
        text = self.tracks[list(self.text_cols)]
        self.reducer, result = pca(numbers_only, self.total_variance_ratio)
        reduced = pd.DataFrame(result)
        reduced[list(self.text_cols)] = text
        return reduced

    @property
    def explained_variance_ratio(self):
        return self.reducer.explained_variance_ratio_
