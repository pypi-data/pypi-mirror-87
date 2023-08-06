__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import numpy as np
import pandas as pd

from mafe.scan import TrackData
from .normalize import normalize


def distances(tracks: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    this_hash, other_hash, distance = [], [], []
    for this_index, this_row in enumerate(tracks[TrackData.columns()].values):
        for other_index, other_row in enumerate(tracks[TrackData.columns()].values):
            if other_index <= this_index:
                continue
            difference = np.subtract(this_row[5:], other_row[5:])
            this_hash.append(this_row[0])
            other_hash.append(other_row[0])
            distance.append(np.linalg.norm(difference))
        if verbose:
            print(
                f"{this_index + 1}/{tracks.shape[0]} len={len(distance)}",
                end="\r", flush=True
            )
    if verbose:
        print()
    return pd.DataFrame.from_dict(
        {'hash_1': this_hash, 'hash_2': other_hash, 'process': distance}
    )


class DistanceCalculator:  # pylint: disable=too-few-public-methods

    def __init__(self, tracks_csv: str, output_filename: str) -> None:
        self.tracks = pd.read_csv(tracks_csv)
        self.output_filename = output_filename

    def run(self, verbose: bool):
        normalized = normalize(self.tracks)
        distances(normalized, verbose=verbose).to_csv(self.output_filename)
