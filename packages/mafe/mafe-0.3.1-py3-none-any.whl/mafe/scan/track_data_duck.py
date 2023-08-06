__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import pandas as pd


class TrackDataDuck:
    """
    Simulate TrackData objects to give mypy type information in TrackDataStorage
    without creating circular imports.
    """

    @property
    def data_frame(self) -> pd.DataFrame:
        """Quack, quack."""
        raise NotImplementedError()

    @property
    def hash(self) -> str:
        raise NotImplementedError()
