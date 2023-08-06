__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from typing import Callable, Tuple

import pandas as pd

from mafe.scan import TrackData

NormalizationFunction = Callable[[pd.DataFrame], pd.DataFrame]


def norm_min_max(frame: pd.DataFrame) -> pd.DataFrame:
    return (frame - frame.min()) / (frame.max() - frame.min())


def norm_zero_max(frame: pd.DataFrame) -> pd.DataFrame:
    zero_min = frame.min().apply(lambda x: min(x, 0))
    return (frame - zero_min) / (frame.max() - zero_min)


def norm_mean(frame: pd.DataFrame) -> pd.DataFrame:
    return (frame - frame.mean()) / frame.std()


NORMALIZATION_FUNCTIONS = {
    'mean': norm_mean,
    'min_max': norm_min_max,
    'zero_max': norm_zero_max
}


def normalize(
        tracks: pd.DataFrame, method: str = 'mean', text_cols: Tuple[str, ...] = None
) -> pd.DataFrame:
    func = NORMALIZATION_FUNCTIONS[method]
    if text_cols is None:
        text_cols = TrackData.STRING_COLUMNS
    numbers_only = tracks.drop(list(text_cols), axis='columns') if text_cols else tracks
    text = tracks[list(text_cols)]
    normalized = func(numbers_only)
    normalized[list(text_cols)] = text
    return normalized
