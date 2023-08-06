__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

# suppress warnings since warnings import interferes with MP3 loading
from contextlib import redirect_stderr
from functools import lru_cache
from hashlib import sha3_224
from logging import info
from pathlib import Path
from typing import Callable, Optional, Tuple

from scipy import stats
import numpy as np
import pandas as pd
import librosa

from .track_metadata import METADATA_COLUMNS, read_track_metadata
from .track_data_duck import TrackDataDuck
from .track_data_storage import TrackDataStorage
from .types import Metadata


class TrackTooLong(ValueError):
    def __init__(self, length: float):
        super().__init__(f"{length:.0f}s > {TrackData.max_track_duration}s")


class TrackData(TrackDataDuck):

    FEATURE_SIZES = dict(
        chroma_stft=12, chroma_cqt=12, chroma_cens=12, tonnetz=6, mfcc=20, rms=1, zcr=1,
        spectral_centroid=1, spectral_bandwidth=1, spectral_contrast=7, spectral_rolloff=1
    )
    MOMENTS = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')
    STRING_COLUMNS = ('hash', 'file_name') + METADATA_COLUMNS
    META_COLUMNS = STRING_COLUMNS + ('tempo', 'duration')

    max_track_duration = 7200

    @classmethod
    def set_max_track_duration(cls, max_duration: int):
        cls.max_track_duration = max_duration

    def __init__(self, storage: TrackDataStorage, track: Path):
        self.track = track
        self.metadata: Metadata = None
        self.feature_series: pd.Series = None
        self._data_frame: pd.DataFrame = None
        with redirect_stderr(None):
            self.load_track(storage, track)

    @property
    def hash(self) -> Optional[str]:
        return str(self.metadata.get('hash')) if self.metadata is not None else None

    @property
    def data_frame(self) -> pd.DataFrame:
        return self._data_frame

    def load_track(self, storage: TrackDataStorage, track: Path):
        metadata = self.read_metadata()
        data_frame = storage.from_hash(str(metadata['hash']))
        if data_frame is not None:
            self._data_frame = data_frame
        else:
            self.load_audio(metadata, track)

    def load_audio(self, metadata, track):
        waveform, sample_rate = librosa.load(str(track))
        metadata.update(self.expensive_metadata(waveform, sample_rate))
        self.metadata = metadata
        self.feature_series = pd.Series(index=TrackData.columns(), dtype=np.float32)
        self.compute_features(waveform, sample_rate)
        self._data_frame = self.feature_series.to_frame().transpose().assign(
            **self.metadata
        )

    @staticmethod
    @lru_cache()
    def columns() -> pd.Index:
        return pd.Index(TrackData.META_COLUMNS + TrackData.stats_columns())

    @staticmethod
    @lru_cache()
    def numerical_columns():
        return ('tempo', 'duration') + TrackData.stats_columns()

    @staticmethod
    @lru_cache()
    def stats_columns() -> Tuple[str, ...]:
        return tuple(sorted([
            f"{name}_{moment}_{i + 1:02d}"
            for name, size in TrackData.FEATURE_SIZES.items()
            for moment in TrackData.MOMENTS
            for i in range(size)
        ]))

    def compute_features(self, waveform: np.ndarray, sample_rate: float) -> None:
        self.feature_stats(
            'zcr', librosa.feature.zero_crossing_rate(waveform, frame_length=2048, hop_length=512)
        )

        cqt = np.abs(librosa.cqt(
            waveform, sr=sample_rate, hop_length=512,
            bins_per_octave=12, n_bins=7 * 12, tuning=None
        ))
        self.feature_stats(
            'chroma_cqt', librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)
        )
        chroma_cens = librosa.feature.chroma_cens(C=cqt, n_chroma=12, n_octaves=7)
        self.feature_stats('chroma_cens', chroma_cens)
        self.feature_stats('tonnetz', librosa.feature.tonnetz(chroma=chroma_cens))

        stft = np.abs(librosa.stft(waveform, n_fft=2048, hop_length=512))
        self.feature_stats('chroma_stft', librosa.feature.chroma_stft(S=stft ** 2, n_chroma=12))
        self.feature_stats('rms', librosa.feature.rms(S=stft))
        self.feature_stats('spectral_centroid', librosa.feature.spectral_centroid(S=stft))
        self.feature_stats('spectral_bandwidth', librosa.feature.spectral_bandwidth(S=stft))
        self.feature_stats(
            'spectral_contrast', librosa.feature.spectral_contrast(S=stft, n_bands=6)
        )
        self.feature_stats('spectral_rolloff', librosa.feature.spectral_rolloff(S=stft))

        mel = librosa.feature.melspectrogram(sr=sample_rate, S=stft ** 2)
        self.feature_stats('mfcc', librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20))

    def feature_stats(self, name: str, values: np.ndarray) -> None:
        self.set_feature(name, values, "mean", np.mean)
        self.set_feature(name, values, "std", np.std)
        self.set_feature(name, values, "skew", stats.skew)
        self.set_feature(name, values, "kurtosis", stats.kurtosis)
        self.set_feature(name, values, "median", np.median)
        self.set_feature(name, values, "min", np.min)
        self.set_feature(name, values, "max", np.max)

    def set_feature(self, name: str, values: np.ndarray, moment: str, function: Callable) -> None:
        for i, value in enumerate(function(values, axis=1)):
            self.feature_series[f"{name}_{moment}_{i + 1:02d}"] = value

    def read_metadata(self) -> Metadata:
        with self.track.open('rb') as file:
            file_hash = sha3_224(file.read()).hexdigest()[:32]
        duration = librosa.get_duration(filename=str(self.track))
        if duration > self.max_track_duration:
            raise TrackTooLong(duration)
        return dict(file_name=self.track.name, hash=file_hash, duration=duration)

    def expensive_metadata(self, waveform: np.ndarray, sample_rate: float) -> Metadata:
        tempo, _ = librosa.beat.beat_track(y=waveform, sr=sample_rate)
        metadata = dict(tempo=tempo)
        try:
            with redirect_stderr(None):
                metadata.update(read_track_metadata(str(self.track)))
        except (RuntimeError, ValueError) as problem:
            info(problem)
        return metadata
        # last.fm stats
        # - loved
        # - num plays
        # - length of period of plays
