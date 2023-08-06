__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import shutil
from pathlib import Path
from time import time
from typing import Callable, Optional, Set

import pandas as pd

from .track_data_duck import TrackDataDuck

DEFAULT_STORE_EVERY = 100


class TrackDataStorage:

    def __init__(
            self, file_name: Path, quiet: bool = False, store_every: int = DEFAULT_STORE_EVERY
    ):
        self.file_name = file_name
        self.quiet = quiet
        self.tracks = self.load()
        self._track_buffer: Set[TrackDataDuck] = set()
        self.store_every = store_every

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._store_buffer()

    @property
    def num_buffered(self) -> int:
        return len(self._track_buffer)

    def load(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.file_name)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame({'hash': []})

    def add_track(self, track: TrackDataDuck) -> None:
        self._track_buffer.add(track)
        if len(self._track_buffer) >= self.store_every:
            self._store_buffer()

    def add_dataframe(self, tracks: pd.DataFrame) -> None:
        hashes_to_add = set(tracks['hash']) - set(self.tracks['hash'])
        tracks_to_add = tracks.loc[tracks['hash'].isin(hashes_to_add)]
        self.tracks = self.tracks.append(tracks_to_add)

    def _store_buffer(self):
        self.store_set(self._track_buffer)
        self._track_buffer = set()

    def store_set(self, tracks: Set[TrackDataDuck]) -> pd.DataFrame:
        if tracks:
            return self.store_dataframe(pd.concat(track.data_frame for track in tracks))
        return self.tracks

    def store_dataframe(self, tracks: pd.DataFrame) -> pd.DataFrame:
        if not tracks.empty:
            self.timed_if_wanted(self.actual_store, tracks)
        return self.tracks

    def actual_store(self, tracks):
        self.add_dataframe(tracks)
        if self.file_name.exists():
            shutil.copy(self.file_name, self.file_name.with_suffix('.old'))
        self.tracks.to_csv(str(self.file_name), compression='infer')

    def from_hash(self, file_hash: str) -> Optional[pd.DataFrame]:
        try:
            found = self.tracks.loc[self.tracks['hash'] == file_hash]
            if found.shape[0] == 0:
                candidates = [track for track in self._track_buffer if track.hash == file_hash]
                if candidates:
                    return candidates[0].data_frame
                return None
            return found
        except KeyError:
            return None

    def timed_if_wanted(self, func: Callable, *args):
        start_time = 0.
        if not self.quiet:
            start_time = time()
            print(f"    Writing tracks to {self.file_name}...", end=' ', flush=True)
        func(*args)
        if not self.quiet:
            elapsed = time() - start_time
            print(f"done ({self.tracks.shape[0]} tracks, {elapsed:.1f}s)")
